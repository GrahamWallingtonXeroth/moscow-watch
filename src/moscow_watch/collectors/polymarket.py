"""Polymarket: full event ladders, historical backfill, and the trade tape.

Three endpoints, three different jobs:

- **Gamma** returns every leg of a multi-leg event in one call. A ceasefire "ladder" is a
  set of legs at different dates, and reading only one of them cannot distinguish a
  parallel shift in sentiment from a change in the market's view of *timing*.
- **CLOB prices-history** returns real history back to market creation, so a baseline does
  not have to be invented.
- **data-api trades** returns the actual fills. This is the difference between "traders
  repriced the war" and "someone bought $400 of a thin market after reading a headline",
  and almost no commentary on prediction markets ever checks it.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from typing import Any
from urllib.parse import urlencode

from ..http import HttpClient
from ..models import stable_id, utc_now_iso

GAMMA_EVENTS = "https://gamma-api.polymarket.com/events"
CLOB_HISTORY = "https://clob.polymarket.com/prices-history"
DATA_TRADES = "https://data-api.polymarket.com/trades"


def _list_value(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return [part.strip() for part in value.split(",") if part.strip()]
        return parsed if isinstance(parsed, list) else []
    return []


def _number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _iso_date(value: Any) -> date | None:
    text = str(value or "")
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        return None


@dataclass(slots=True)
class Leg:
    """One rung of a Polymarket event ladder."""

    market_id: str
    event_slug: str
    captured_at: str
    question: str
    market_slug: str
    condition_id: str
    group_item_title: str
    end_date: str
    yes_price: float | None
    no_price: float | None
    best_bid: float | None = None
    best_ask: float | None = None
    last_trade_price: float | None = None
    spread: float | None = None
    volume: float | None = None
    liquidity: float | None = None
    outcomes: list[str] = field(default_factory=list)
    clob_token_ids: list[str] = field(default_factory=list)
    closed: bool | None = None
    active: bool | None = None
    archived: bool | None = None
    source_url: str = ""
    source: str = "polymarket_gamma"

    @property
    def id(self) -> str:
        return stable_id("pm_leg", self.market_slug or self.condition_id, self.captured_at)

    @property
    def resolves(self) -> date | None:
        return _iso_date(self.end_date)

    def token_for(self, outcome: str) -> str:
        for index, name in enumerate(self.outcomes):
            if str(name).casefold() == outcome.casefold():
                return str(self.clob_token_ids[index]) if index < len(self.clob_token_ids) else ""
        return ""

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, **asdict(self)}


@dataclass(slots=True)
class HistoryPoint:
    """A real historical price, distinguishable from live collection by `source`."""

    token_id: str
    market_id: str
    timestamp: int
    observed_at: str
    price: float
    source: str = "polymarket_prices_history"

    @property
    def id(self) -> str:
        return stable_id("pm_hist", self.token_id, self.timestamp)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, **asdict(self)}


@dataclass(slots=True)
class Trade:
    condition_id: str
    market_id: str
    timestamp: int
    traded_at: str
    price: float
    size: float
    side: str
    outcome: str
    transaction_hash: str = ""
    source: str = "polymarket_trades"

    @property
    def id(self) -> str:
        return stable_id("pm_trade", self.transaction_hash or "", self.timestamp, self.size)

    @property
    def notional(self) -> float:
        return round(self.price * self.size, 4)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "notional": self.notional, **asdict(self)}


def _epoch_to_iso(seconds: Any) -> str:
    try:
        return (
            datetime.fromtimestamp(int(seconds), UTC)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
    except (TypeError, ValueError, OSError, OverflowError):
        return ""


def parse_event(payload: Any, event_slug: str, captured_at: str) -> list[Leg]:
    """Every leg of the event, including closed ones; callers decide what to keep."""
    event = payload[0] if isinstance(payload, list) and payload else payload
    if not isinstance(event, dict):
        raise ValueError(f"unexpected Gamma response for {event_slug}")
    markets = event.get("markets") or []
    if not isinstance(markets, list) or not markets:
        raise ValueError(f"no markets found for event {event_slug}")

    legs: list[Leg] = []
    for raw in markets:
        if not isinstance(raw, dict):
            continue
        outcomes = [str(x) for x in _list_value(raw.get("outcomes"))]
        prices = [
            value for value in (_number(x) for x in _list_value(raw.get("outcomePrices")))
            if value is not None
        ]
        if len(prices) != len(outcomes):
            # Resolved legs sometimes drop their prices entirely. Skipping such a leg is
            # correct; failing the whole ladder because one settled rung is malformed is
            # not. Live legs are still held to the strict rule below.
            if raw.get("closed") is True or not prices:
                continue
            # Never guess which price belongs to which outcome.
            raise ValueError(
                f"{event_slug}: {len(outcomes)} outcomes but {len(prices)} prices for "
                f"{raw.get('slug')}"
            )
        by_outcome = {name.casefold(): value for name, value in zip(outcomes, prices, strict=True)}
        best_bid = _number(raw.get("bestBid"))
        best_ask = _number(raw.get("bestAsk"))
        spread = _number(raw.get("spread"))
        if spread is None and best_bid is not None and best_ask is not None:
            spread = round(best_ask - best_bid, 6)
        legs.append(
            Leg(
                market_id=f"polymarket:{raw.get('slug') or raw.get('conditionId')}",
                event_slug=event_slug,
                captured_at=captured_at,
                question=str(raw.get("question") or ""),
                market_slug=str(raw.get("slug") or ""),
                condition_id=str(raw.get("conditionId") or ""),
                group_item_title=str(raw.get("groupItemTitle") or ""),
                end_date=str(raw.get("endDate") or ""),
                yes_price=by_outcome.get("yes"),
                no_price=by_outcome.get("no"),
                best_bid=best_bid,
                best_ask=best_ask,
                last_trade_price=_number(raw.get("lastTradePrice")),
                spread=spread,
                volume=_number(raw.get("volumeNum") or raw.get("volume")),
                liquidity=_number(raw.get("liquidityNum") or raw.get("liquidity")),
                outcomes=outcomes,
                clob_token_ids=[str(x) for x in _list_value(raw.get("clobTokenIds"))],
                closed=_bool(raw.get("closed")),
                active=_bool(raw.get("active")),
                archived=_bool(raw.get("archived")),
                source_url=f"https://polymarket.com/event/{event_slug}",
            )
        )
    return legs


def open_legs(legs: list[Leg], *, today: date | None = None) -> list[Leg]:
    """Legs that are still tradable. A resolved rung is not part of a live term structure."""
    reference = today or datetime.now(UTC).date()
    keep: list[Leg] = []
    for leg in legs:
        if leg.closed is True or leg.archived is True or leg.active is False:
            continue
        resolves = leg.resolves
        if resolves is not None and resolves <= reference:
            continue
        keep.append(leg)
    keep.sort(key=lambda leg: (leg.resolves or date.max))
    return keep


def parse_history(payload: Any, token_id: str, market_id: str) -> list[HistoryPoint]:
    if not isinstance(payload, dict):
        raise ValueError(f"unexpected prices-history response for {token_id}")
    points: list[HistoryPoint] = []
    for raw in payload.get("history") or []:
        if not isinstance(raw, dict):
            continue
        price = _number(raw.get("p"))
        timestamp = raw.get("t")
        if price is None or timestamp is None:
            continue
        points.append(
            HistoryPoint(
                token_id=token_id,
                market_id=market_id,
                timestamp=int(timestamp),
                observed_at=_epoch_to_iso(timestamp),
                price=price,
            )
        )
    points.sort(key=lambda p: p.timestamp)
    return points


def parse_trades(payload: Any, condition_id: str, market_id: str) -> list[Trade]:
    if not isinstance(payload, list):
        raise ValueError(f"unexpected trades response for {condition_id}")
    trades: list[Trade] = []
    for raw in payload:
        if not isinstance(raw, dict):
            continue
        price = _number(raw.get("price"))
        size = _number(raw.get("size"))
        timestamp = raw.get("timestamp")
        if price is None or size is None or timestamp is None:
            continue
        trades.append(
            Trade(
                condition_id=condition_id,
                market_id=market_id,
                timestamp=int(timestamp),
                traded_at=_epoch_to_iso(timestamp),
                price=price,
                size=size,
                side=str(raw.get("side") or ""),
                outcome=str(raw.get("outcome") or ""),
                transaction_hash=str(raw.get("transactionHash") or ""),
            )
        )
    trades.sort(key=lambda t: t.timestamp)
    return trades


def tape_summary(trades: list[dict[str, Any]]) -> dict[str, Any]:
    """Was a move backed by size, or by a handful of small orders?"""
    if not trades:
        return {"trades": 0, "notional": 0.0, "median_notional": None, "largest_notional": None}
    notionals = sorted(float(t.get("notional") or 0.0) for t in trades)
    middle = len(notionals) // 2
    median = (
        notionals[middle]
        if len(notionals) % 2
        else (notionals[middle - 1] + notionals[middle]) / 2
    )
    return {
        "trades": len(trades),
        "notional": round(sum(notionals), 2),
        "median_notional": round(median, 2),
        "largest_notional": round(notionals[-1], 2),
    }


class PolymarketCollector:
    def __init__(self, client: HttpClient | None = None) -> None:
        self.client = client or HttpClient()

    def ladder(self, event_slug: str, *, captured_at: str = "") -> list[Leg]:
        query = urlencode({"slug": event_slug})
        payload = self.client.get_json(f"{GAMMA_EVENTS}?{query}")
        return parse_event(payload, event_slug, captured_at or utc_now_iso())

    def history(
        self, token_id: str, *, market_id: str = "", interval: str = "max", fidelity: int = 60
    ) -> list[HistoryPoint]:
        query = urlencode(
            {"market": token_id, "interval": interval, "fidelity": int(fidelity)}
        )
        payload = self.client.get_json(f"{CLOB_HISTORY}?{query}")
        return parse_history(payload, token_id, market_id or token_id)

    def trades(self, condition_id: str, *, market_id: str = "", limit: int = 200) -> list[Trade]:
        query = urlencode({"market": condition_id, "limit": min(max(limit, 1), 1000)})
        payload = self.client.get_json(f"{DATA_TRADES}?{query}")
        return parse_trades(payload, condition_id, market_id or condition_id)
