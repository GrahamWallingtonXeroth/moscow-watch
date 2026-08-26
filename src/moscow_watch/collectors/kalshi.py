"""Kalshi markets, order books and candlesticks.

Kalshi publishes machine-readable resolution wording. That is unusual and valuable: a
change to `rules_primary` or to an event's settlement sources changes what a price
*means*, and a tracker that quietly kept plotting the old series through such a change
would be misleading. So the wording is stored verbatim on first sight and diffed on every
run.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from urllib.parse import urlencode

from ..http import HttpClient
from ..models import stable_id, utc_now_iso

BASE = "https://external-api.kalshi.com/trade-api/v2"

# Kalshi accepts only these candlestick periods, in minutes.
VALID_PERIODS = (1, 60, 1440)


def _number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _dollars(value: Any) -> float | None:
    """Kalshi quotes `*_dollars` as decimal strings already in [0, 1]. Do not rescale."""
    number = _number(value)
    return None if number is None else round(number, 6)


@dataclass(slots=True)
class KalshiMarket:
    market_id: str
    ticker: str
    series_ticker: str
    event_ticker: str
    title: str
    captured_at: str
    status: str = ""
    close_time: str = ""
    yes_bid: float | None = None
    yes_ask: float | None = None
    last_price: float | None = None
    volume: float | None = None
    open_interest: float | None = None
    liquidity: float | None = None
    rules_primary: str = ""
    rules_secondary: str = ""
    settlement_sources: list[str] = field(default_factory=list)
    source_url: str = ""
    source: str = "kalshi"

    @property
    def id(self) -> str:
        return stable_id("kalshi", self.ticker, self.captured_at)

    @property
    def rules_fingerprint(self) -> str:
        """Stable hash of the resolution wording, so a change is detectable."""
        return stable_id(
            "rules", self.rules_primary, self.rules_secondary, "|".join(self.settlement_sources)
        )

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "rules_fingerprint": self.rules_fingerprint, **asdict(self)}


@dataclass(slots=True)
class KalshiCandle:
    ticker: str
    end_period_ts: int
    open_dollars: float | None
    high_dollars: float | None
    low_dollars: float | None
    close_dollars: float | None
    volume: float | None
    open_interest: float | None
    source: str = "kalshi_candlesticks"

    @property
    def id(self) -> str:
        return stable_id("kalshi_candle", self.ticker, self.end_period_ts)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, **asdict(self)}


def parse_settlement_sources(payload: Any) -> list[str]:
    """Settlement sources live on the event, not the market."""
    event = (payload or {}).get("event") if isinstance(payload, dict) else None
    out: list[str] = []
    for source in (event or {}).get("settlement_sources") or []:
        if isinstance(source, dict):
            name = str(source.get("name") or "").strip()
            url = str(source.get("url") or "").strip()
            out.append(f"{name} <{url}>" if name and url else name or url)
        else:
            out.append(str(source))
    return [item for item in out if item]


def parse_markets(
    payload: Any,
    series_ticker: str,
    captured_at: str,
    settlement_sources: dict[str, list[str]] | None = None,
) -> list[KalshiMarket]:
    if not isinstance(payload, dict):
        raise ValueError(f"unexpected Kalshi markets response for {series_ticker}")
    out: list[KalshiMarket] = []
    for raw in payload.get("markets") or []:
        if not isinstance(raw, dict):
            continue
        ticker = str(raw.get("ticker") or "")
        if not ticker:
            continue
        event_ticker = str(raw.get("event_ticker") or "")
        names = settlement_sources.get(event_ticker, []) if settlement_sources else []
        out.append(
            KalshiMarket(
                market_id=f"kalshi:{ticker}",
                ticker=ticker,
                series_ticker=series_ticker,
                title=str(raw.get("title") or ""),
                captured_at=captured_at,
                status=str(raw.get("status") or ""),
                event_ticker=event_ticker,
                close_time=str(raw.get("close_time") or ""),
                yes_bid=_dollars(raw.get("yes_bid_dollars")),
                yes_ask=_dollars(raw.get("yes_ask_dollars")),
                last_price=_dollars(raw.get("last_price_dollars")),
                volume=_number(raw.get("volume_fp")),
                open_interest=_number(raw.get("open_interest_fp")),
                liquidity=_number(raw.get("liquidity_dollars")),
                rules_primary=str(raw.get("rules_primary") or ""),
                rules_secondary=str(raw.get("rules_secondary") or ""),
                settlement_sources=names,
                source_url=f"https://kalshi.com/markets/{ticker}",
            )
        )
    return out


def parse_candlesticks(payload: Any, ticker: str) -> list[KalshiCandle]:
    if not isinstance(payload, dict):
        raise ValueError(f"unexpected Kalshi candlestick response for {ticker}")
    out: list[KalshiCandle] = []
    for raw in payload.get("candlesticks") or []:
        if not isinstance(raw, dict):
            continue
        price = raw.get("price") or {}
        out.append(
            KalshiCandle(
                ticker=ticker,
                end_period_ts=int(raw.get("end_period_ts") or 0),
                open_dollars=_number(price.get("open_dollars")),
                high_dollars=_number(price.get("high_dollars")),
                low_dollars=_number(price.get("low_dollars")),
                close_dollars=_number(price.get("close_dollars")),
                volume=_number(raw.get("volume_fp")),
                open_interest=_number(raw.get("open_interest_fp")),
            )
        )
    return out


class KalshiCollector:
    def __init__(self, client: HttpClient | None = None) -> None:
        self.client = client or HttpClient()

    def event_settlement_sources(self, event_ticker: str) -> list[str]:
        payload = self.client.get_json(f"{BASE}/events/{event_ticker}")
        return parse_settlement_sources(payload)

    def series(
        self,
        series_ticker: str,
        *,
        status: str = "open",
        limit: int = 200,
        captured_at: str = "",
        with_settlement_sources: bool = True,
    ) -> list[KalshiMarket]:
        query = urlencode(
            {"series_ticker": series_ticker, "status": status, "limit": min(max(limit, 1), 1000)}
        )
        payload = self.client.get_json(f"{BASE}/markets?{query}")
        sources: dict[str, list[str]] = {}
        if with_settlement_sources and isinstance(payload, dict):
            # One call per distinct event, not per market.
            for event_ticker in {
                str(m.get("event_ticker") or "")
                for m in payload.get("markets") or []
                if isinstance(m, dict) and m.get("event_ticker")
            }:
                try:
                    sources[event_ticker] = self.event_settlement_sources(event_ticker)
                except Exception:
                    sources[event_ticker] = []
        return parse_markets(payload, series_ticker, captured_at or utc_now_iso(), sources)

    def orderbook(self, ticker: str) -> dict[str, Any]:
        payload = self.client.get_json(f"{BASE}/markets/{ticker}/orderbook")
        return payload if isinstance(payload, dict) else {}

    def candlesticks(
        self, series_ticker: str, ticker: str, *, start_ts: int, end_ts: int, period: int = 1440
    ) -> list[KalshiCandle]:
        if period not in VALID_PERIODS:
            raise ValueError(f"period must be one of {VALID_PERIODS} minutes")
        # All three parameters are required by the endpoint; omitting any returns an error.
        query = urlencode(
            {"start_ts": int(start_ts), "end_ts": int(end_ts), "period_interval": period}
        )
        payload = self.client.get_json(
            f"{BASE}/series/{series_ticker}/markets/{ticker}/candlesticks?{query}"
        )
        return parse_candlesticks(payload, ticker)


def rules_changes(
    previous: list[dict[str, Any]], current: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Detect changed resolution wording and newly listed markets in a tracked series.

    A change here is a material event: the same ticker can silently start meaning
    something different.
    """
    if not previous:
        # First sighting of a series is not a change. Reporting every market as "new" on
        # the first run would bury the one line that actually matters later.
        return []

    last_by_ticker: dict[str, dict[str, Any]] = {}
    for row in previous:
        ticker = str(row.get("ticker") or "")
        if not ticker:
            continue
        seen = last_by_ticker.get(ticker)
        if seen is None or str(row.get("captured_at", "")) > str(seen.get("captured_at", "")):
            last_by_ticker[ticker] = row

    changes: list[dict[str, Any]] = []
    for row in current:
        ticker = str(row.get("ticker") or "")
        before = last_by_ticker.get(ticker)
        if before is None:
            changes.append(
                {
                    "kind": "new_market",
                    "ticker": ticker,
                    "series_ticker": row.get("series_ticker", ""),
                    "title": row.get("title", ""),
                    "close_time": row.get("close_time", ""),
                }
            )
            continue
        if before.get("rules_fingerprint") != row.get("rules_fingerprint"):
            changes.append(
                {
                    "kind": "rules_changed",
                    "ticker": ticker,
                    "series_ticker": row.get("series_ticker", ""),
                    "title": row.get("title", ""),
                    "before": str(before.get("rules_primary", ""))[:400],
                    "after": str(row.get("rules_primary", ""))[:400],
                    "settlement_sources_before": before.get("settlement_sources", []),
                    "settlement_sources_after": row.get("settlement_sources", []),
                }
            )
    return changes
