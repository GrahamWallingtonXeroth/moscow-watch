from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(UTC)


def hours_since(value: str, *, now: datetime | None = None) -> float | None:
    try:
        moment = parse_time(value)
    except (TypeError, ValueError):
        return None
    reference = now or datetime.now(UTC)
    return (reference - moment).total_seconds() / 3600.0


def stable_id(*parts: object, length: int = 20) -> str:
    payload = "\x1f".join(str(part) for part in parts)
    return sha256(payload.encode("utf-8")).hexdigest()[:length]


@dataclass(slots=True)
class MarketSnapshot:
    """One real observation of one currently tradable Polymarket market."""

    market_id: str
    captured_at: str
    probability: float
    title: str
    event_slug: str
    question: str = ""
    market_slug: str = ""
    condition_id: str = ""
    end_date: str = ""
    active: bool | None = None
    closed: bool | None = None
    archived: bool | None = None
    accepting_orders: bool | None = None
    resolution_source: str = ""
    outcomes: list[str] = field(default_factory=list)
    outcome_prices: list[float] = field(default_factory=list)
    clob_token_ids: list[str] = field(default_factory=list)
    volume: float | None = None
    liquidity: float | None = None
    volume_24h: float | None = None
    best_bid: float | None = None
    best_ask: float | None = None
    spread: float | None = None
    source_url: str = ""
    source: str = "polymarket_gamma"
    note: str = ""

    @property
    def id(self) -> str:
        return stable_id(self.market_id, self.captured_at)

    def token_for(self, outcome: str) -> str:
        """Return the CLOB token id whose index matches the named outcome."""
        for index, name in enumerate(self.outcomes):
            if str(name).casefold() == outcome.casefold():
                if index < len(self.clob_token_ids):
                    return str(self.clob_token_ids[index])
                return ""
        return ""

    def price_for(self, outcome: str) -> float | None:
        for index, name in enumerate(self.outcomes):
            if str(name).casefold() == outcome.casefold():
                if index < len(self.outcome_prices):
                    return float(self.outcome_prices[index])
                return None
        return None

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, **asdict(self)}


@dataclass(slots=True)
class NewsItem:
    """One article from a configured, robots-permitted source.

    `source_family` is the unit of editorial independence and `source_type` decides what
    the item is allowed to establish. Both travel with the record so the promotion rules
    never have to guess.
    """

    source_id: str
    title: str
    url: str
    published_at: str
    publisher: str
    source_family: str = ""
    source_type: str = "independent_reporting"
    standpoint: str = ""
    domain: str = ""
    summary: str = ""
    discovery_route: str = ""
    language: str = ""
    collected_at: str = field(default_factory=utc_now_iso)

    @property
    def id(self) -> str:
        # Keyed on canonical URL only, so re-discovering the same article never duplicates it.
        return stable_id("news", self.url or f"{self.source_id}:{self.title}")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, **asdict(self)}


@dataclass(slots=True)
class EvidenceReview:
    """A deterministic classification of one article against one hypothesis."""

    candidate_id: str
    hypothesis_id: str
    verdict: str
    confidence: float
    note: str
    reviewer: str = "auto"
    signal_id: str = ""
    matched_terms: list[str] = field(default_factory=list)
    basis: str = "headline rule"
    reviewed_at: str = field(default_factory=utc_now_iso)

    @property
    def id(self) -> str:
        # Deliberately excludes time: re-running the same rule on the same article is idempotent.
        return stable_id(self.candidate_id, self.hypothesis_id, self.reviewer, self.signal_id)

    def validate(self) -> None:
        if self.verdict not in {"supports", "refutes", "neutral"}:
            raise ValueError("verdict must be supports, refutes, or neutral")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {"id": self.id, **asdict(self)}


@dataclass(slots=True)
class RuleResult:
    rule_id: str
    hypothesis_id: str
    status: str
    contribution: float
    detail: str
    evaluated_at: str = field(default_factory=utc_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SourceStatus:
    """Current health of one source. Overwritten in place, never appended."""

    source_id: str
    kind: str
    label: str
    status: str = "unknown"
    last_attempt_at: str = ""
    last_success_at: str = ""
    records: int = 0
    error_category: str = ""
    error_message: str = ""
    target: str = ""
    source_family: str = ""
    consecutive_failures: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def is_stale(last_success_at: str, threshold_hours: float, *, now: datetime | None = None) -> bool:
    if not last_success_at:
        return True
    age = hours_since(last_success_at, now=now)
    return age is None or age > threshold_hours


def within_window(published_at: str, hours: float, *, now: datetime | None = None) -> bool:
    if not published_at:
        return False
    try:
        moment = parse_time(published_at)
    except (TypeError, ValueError):
        return False
    reference = now or datetime.now(UTC)
    return moment >= reference - timedelta(hours=hours)
