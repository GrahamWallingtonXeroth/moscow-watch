"""Configuration for `indicators.toml`.

The unit here is an **indicator**: a named quantity, from a named source, with a value, a
timestamp, a date on which it becomes decidable, and a stated direction of implication for
each hypothesis. There are no rules that adjudicate anything. Nothing is weighted, scored
or summed. A human does the interpreting, in the articles, under their own name.
"""

from __future__ import annotations

import re
import tomllib
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

SOURCE_TYPES = {"primary_record", "independent_reporting", "discovery_only"}
CLAIM_TYPES = {"official_action", "actor_statement", "external_observable", "allegation"}
INDICATOR_KINDS = {
    "market_probability",   # a prediction-market price
    "market_ladder",        # a set of dated legs read as a term structure
    "counted_quantity",     # something physically counted, e.g. ship transits
    "event_count",          # a tally built from collected records, e.g. contacts
    "reporting_index",      # how much a subject is being reported, from a news index
}
DIRECTIONS = {"up", "down", "flat"}
VENUES = {"polymarket", "kalshi", "portwatch", "corpus", "gdelt"}


@dataclass(slots=True)
class Hypothesis:
    id: str
    name: str
    claim: str
    falsifier: str = ""
    falsifier_date: str = ""
    scored: bool = True
    note: str = ""


@dataclass(slots=True)
class Bearing:
    """Which way an indicator moving would point, for one hypothesis."""

    hypothesis: str
    direction: str


@dataclass(slots=True)
class Indicator:
    id: str
    name: str
    source: str
    kind: str
    resolves: str = ""
    ticker: str = ""
    event_slug: str = ""
    series_ticker: str = ""
    chokepoint_id: str = ""
    query: str = ""
    value_field: str = ""
    material_move: float = 0.05
    bears_on: list[dict[str, str]] = field(default_factory=list)
    note: str = ""
    enabled: bool = True
    disabled_reason: str = ""

    @property
    def resolves_date(self) -> date | None:
        try:
            return date.fromisoformat(self.resolves) if self.resolves else None
        except ValueError:
            return None

    @property
    def bearings(self) -> list[Bearing]:
        return [
            Bearing(hypothesis=str(b.get("hypothesis", "")), direction=str(b.get("direction", "")))
            for b in self.bears_on
        ]


@dataclass(slots=True)
class NewsSource:
    id: str
    title: str
    url: str
    publisher: str
    source_family: str
    source_type: str = "independent_reporting"
    standpoint: str = ""
    enabled: bool = True
    disabled_reason: str = ""
    reference_url: str = ""
    include_any: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DiscoveryQuery:
    id: str
    title: str
    query: str
    max_records: int = 250
    enabled: bool = True


@dataclass(slots=True)
class ClaimRule:
    id: str
    title: str
    hypothesis_id: str
    claim_type: str = "external_observable"
    required_groups: list[list[str]] = field(default_factory=list)
    excluded_any: list[str] = field(default_factory=list)
    corroboration_window_hours: float = 48.0
    basis: str = "headline and summary rule"
    # Kept for compatibility with the corroboration engine's signature; unused for scoring.
    verdict: str = "bears_on"


@dataclass(slots=True)
class Config:
    project: dict[str, Any]
    hypotheses: list[Hypothesis]
    indicators: list[Indicator]
    news_sources: list[NewsSource]
    discovery_queries: list[DiscoveryQuery]
    claim_rules: list[ClaimRule]

    @property
    def news_timespan_hours(self) -> float:
        return _timespan_hours(str(self.project.get("news_timespan", "3d")))

    @property
    def stale_after_hours(self) -> float:
        return float(self.project.get("stale_after_hours", 12))

    @property
    def min_change_window_hours(self) -> float:
        """Never report a move computed over a shorter window than this."""
        return float(self.project.get("min_change_window_hours", 6))

    @property
    def max_discovery_queries(self) -> int:
        return int(self.project.get("max_discovery_queries", 2))

    @property
    def discovery_min_interval_seconds(self) -> float:
        return float(self.project.get("discovery_min_interval_seconds", 6.0))

    @property
    def contact_anchor(self) -> date:
        return date.fromisoformat(str(self.project.get("contact_anchor", "2026-01-05")))

    @property
    def engagement_baseline_start(self) -> date:
        return date.fromisoformat(
            str(self.project.get("engagement_baseline_start", "2026-01-01"))
        )

    @property
    def engagement_baseline_end(self) -> date:
        """The last day of the baseline window: the day before the event, never after it."""
        stated = date.fromisoformat(
            str(self.project.get("engagement_baseline_end", "2026-08-24"))
        )
        return min(stated, self.event_date - timedelta(days=1))

    @property
    def event_date(self) -> date:
        return date.fromisoformat(str(self.project.get("event_date", "2026-08-25")))

    @property
    def enabled_indicators(self) -> list[Indicator]:
        return [i for i in self.indicators if i.enabled]

    @property
    def enabled_news_sources(self) -> list[NewsSource]:
        return [s for s in self.news_sources if s.enabled]

    @property
    def enabled_discovery(self) -> list[DiscoveryQuery]:
        return [q for q in self.discovery_queries if q.enabled][: self.max_discovery_queries]

    @property
    def reporting_families(self) -> set[str]:
        return {
            s.source_family
            for s in self.enabled_news_sources
            if s.source_type == "independent_reporting"
        }

    def indicators_for(self, source: str) -> list[Indicator]:
        return [i for i in self.enabled_indicators if i.source == source]

    def hypothesis(self, hypothesis_id: str) -> Hypothesis | None:
        return next((h for h in self.hypotheses if h.id == hypothesis_id), None)


_TIMESPAN = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*([hdwm])\s*$", re.IGNORECASE)
_UNITS = {"h": 1.0, "d": 24.0, "w": 168.0, "m": 720.0}


def _timespan_hours(value: str) -> float:
    match = _TIMESPAN.match(value)
    if not match:
        raise ValueError(f"invalid timespan {value!r}; use forms like 12h, 3d, 1w")
    return float(match.group(1)) * _UNITS[match.group(2).casefold()]


def timespan_label(hours: float) -> str:
    return f"{int(hours // 24)}d" if hours % 24 == 0 else f"{int(hours)}h"


def _build(cls, items: list[dict[str, Any]], label: str):
    built = []
    for item in items:
        try:
            built.append(cls(**item))
        except TypeError as exc:
            raise ValueError(
                f"invalid [[{label}]] entry {item.get('id', '<unnamed>')}: {exc}"
            ) from exc
    return built


def load_config(path: str | Path) -> Config:
    with Path(path).open("rb") as handle:
        raw = tomllib.load(handle)
    return Config(
        project=raw.get("project", {}),
        hypotheses=_build(Hypothesis, raw.get("hypotheses", []), "hypotheses"),
        indicators=_build(Indicator, raw.get("indicators", []), "indicators"),
        news_sources=_build(NewsSource, raw.get("news_sources", []), "news_sources"),
        discovery_queries=_build(
            DiscoveryQuery, raw.get("discovery_queries", []), "discovery_queries"
        ),
        claim_rules=_build(ClaimRule, raw.get("claim_rules", []), "claim_rules"),
    )


def _duplicates(ids: list[str]) -> list[str]:
    seen: set[str] = set()
    dupes: list[str] = []
    for item in ids:
        if item in seen and item not in dupes:
            dupes.append(item)
        seen.add(item)
    return dupes


def validate_config(config: Config) -> list[str]:
    errors: list[str] = []

    try:
        _ = config.news_timespan_hours
    except ValueError as exc:
        errors.append(f"[project] {exc}")
    for key, value in (
        ("stale_after_hours", config.stale_after_hours),
        ("min_change_window_hours", config.min_change_window_hours),
    ):
        if value <= 0:
            errors.append(f"[project] {key} must be positive")
    if config.discovery_min_interval_seconds < 5:
        errors.append(
            "[project] discovery_min_interval_seconds must be at least 5 to respect GDELT's "
            "documented rate limit"
        )
    for key in (
        "contact_anchor",
        "event_date",
        "engagement_baseline_start",
        "engagement_baseline_end",
    ):
        try:
            getattr(config, key)
        except (ValueError, TypeError):
            errors.append(f"[project] {key} must be an ISO date")

    try:
        if config.engagement_baseline_start >= config.engagement_baseline_end:
            errors.append(
                "[project] engagement_baseline_start must precede engagement_baseline_end"
            )
    except (ValueError, TypeError):
        pass

    hypothesis_ids = {h.id for h in config.hypotheses}
    for dupe in _duplicates([h.id for h in config.hypotheses]):
        errors.append(f"duplicate hypothesis id: {dupe}")
    for hypothesis in config.hypotheses:
        if hypothesis.scored and not hypothesis.falsifier:
            errors.append(f"hypothesis {hypothesis.id} is tracked but states no falsifier")
        if hypothesis.falsifier_date:
            try:
                date.fromisoformat(hypothesis.falsifier_date)
            except ValueError:
                errors.append(f"hypothesis {hypothesis.id} has a non-ISO falsifier_date")

    for dupe in _duplicates([i.id for i in config.indicators]):
        errors.append(f"duplicate indicator id: {dupe}")
    for indicator in config.indicators:
        if indicator.kind not in INDICATOR_KINDS:
            errors.append(
                f"indicator {indicator.id} has invalid kind {indicator.kind!r}; "
                f"expected one of {sorted(INDICATOR_KINDS)}"
            )
        if indicator.source not in VENUES:
            errors.append(
                f"indicator {indicator.id} has invalid source {indicator.source!r}; "
                f"expected one of {sorted(VENUES)}"
            )
        if not 0 < indicator.material_move <= 1:
            errors.append(
                f"indicator {indicator.id} material_move must be in (0, 1]; it is the "
                "threshold below which a move is not reported"
            )
        if indicator.resolves and indicator.resolves_date is None:
            errors.append(f"indicator {indicator.id} has a non-ISO resolves date")
        if not indicator.bears_on:
            errors.append(
                f"indicator {indicator.id} bears on no hypothesis; an indicator that "
                "discriminates nothing should not be tracked"
            )
        for bearing in indicator.bearings:
            if bearing.hypothesis not in hypothesis_ids:
                errors.append(
                    f"indicator {indicator.id} bears on unknown hypothesis "
                    f"{bearing.hypothesis!r}"
                )
            if bearing.direction not in DIRECTIONS:
                errors.append(
                    f"indicator {indicator.id} has invalid direction {bearing.direction!r}; "
                    f"expected one of {sorted(DIRECTIONS)}"
                )
        if indicator.source == "gdelt" and not indicator.query:
            errors.append(
                f"indicator {indicator.id} draws on GDELT but states no query; the query is "
                "the whole definition of a reporting-volume series"
            )
        if not indicator.enabled and not indicator.disabled_reason:
            errors.append(f"indicator {indicator.id} is disabled but gives no disabled_reason")

    for dupe in _duplicates([s.id for s in config.news_sources]):
        errors.append(f"duplicate news_source id: {dupe}")
    for source in config.news_sources:
        if source.source_type not in SOURCE_TYPES:
            errors.append(f"news source {source.id} has invalid source_type {source.source_type!r}")
        if not source.source_family:
            errors.append(f"news source {source.id} has no source_family")
        if source.source_type == "primary_record" and not source.standpoint:
            errors.append(f"primary source {source.id} must declare a standpoint")
        if not source.enabled and not source.disabled_reason:
            errors.append(f"news source {source.id} is disabled but gives no disabled_reason")
    if len(config.reporting_families) < 2:
        errors.append(
            "at least two independent reporting families must be enabled, otherwise no "
            "external claim can ever be corroborated"
        )

    for dupe in _duplicates([q.id for q in config.discovery_queries]):
        errors.append(f"duplicate discovery_query id: {dupe}")
    for query in config.discovery_queries:
        if "domain:reuters.com" in query.query:
            errors.append(
                f"discovery query {query.id} filters on domain:reuters.com, which returns "
                "nothing from GDELT"
            )

    for dupe in _duplicates([r.id for r in config.claim_rules]):
        errors.append(f"duplicate claim_rule id: {dupe}")
    for rule in config.claim_rules:
        if rule.hypothesis_id not in hypothesis_ids:
            errors.append(f"claim rule {rule.id} references unknown hypothesis {rule.hypothesis_id}")
        if rule.claim_type not in CLAIM_TYPES:
            errors.append(f"claim rule {rule.id} has invalid claim_type {rule.claim_type!r}")
        if not rule.required_groups:
            errors.append(f"claim rule {rule.id} must define at least one required group")
        for index, group in enumerate(rule.required_groups):
            if not isinstance(group, list) or not group:
                errors.append(f"claim rule {rule.id} required group {index} is empty")
    return errors
