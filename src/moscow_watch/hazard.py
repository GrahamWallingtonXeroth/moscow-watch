"""Term-structure maths for a ladder of cumulative-probability markets.

A ceasefire ladder prices "a deal by date D" for several D. Those raw numbers rise with
time simply because a longer window contains more chances, so comparing them directly
says almost nothing. Converting each rung to a *forward conditional hazard* — the chance
of the event arriving inside that window given it has not arrived yet — strips the window
length out and makes the rungs comparable.

That matters for reading news: a parallel shift in the ladder is sentiment, a change in
the *shape* is new information about timing.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any

# A window shorter than this sits within a few exchange ticks of zero, so its implied
# hazard is dominated by the tick size rather than by any belief about timing.
MIN_INFORMATIVE_WINDOW_DAYS = 14


@dataclass(slots=True)
class Rung:
    """One leg of a ladder: the cumulative probability of the event by `resolves`."""

    label: str
    resolves: date
    cumulative: float
    source: str = ""
    ticker: str = ""


@dataclass(slots=True)
class HazardPoint:
    label: str
    resolves: str
    window_days: int
    cumulative: float
    forward_conditional: float
    hazard_per_day: float
    monthly_equivalent: float
    informative: bool
    excluded_because: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class HazardCurve:
    points: list[HazardPoint] = field(default_factory=list)
    excluded: list[str] = field(default_factory=list)
    as_of: str = ""

    @property
    def informative(self) -> list[HazardPoint]:
        return [p for p in self.points if p.informative]

    @property
    def peak(self) -> HazardPoint | None:
        candidates = self.informative
        return max(candidates, key=lambda p: p.monthly_equivalent) if candidates else None

    @property
    def trough(self) -> HazardPoint | None:
        candidates = self.informative
        return min(candidates, key=lambda p: p.monthly_equivalent) if candidates else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "as_of": self.as_of,
            "points": [p.to_dict() for p in self.points],
            "excluded": list(self.excluded),
        }


def forward_conditional(previous: float, current: float) -> float:
    """P(event in this window | not yet by the previous date).

    Returns 0.0 rather than a negative number when a ladder is non-monotone, which happens
    with real quotes because adjacent legs trade independently.
    """
    if not 0.0 <= previous <= 1.0 or not 0.0 <= current <= 1.0:
        raise ValueError("cumulative probabilities must lie in [0, 1]")
    remaining = 1.0 - previous
    if remaining <= 0.0:
        # The event is already priced as certain; nothing is left to happen.
        return 0.0
    return max(0.0, (current - previous) / remaining)


def hazard_per_day(conditional: float, days: int) -> float:
    """Constant per-day hazard implied by `conditional` arriving over `days`."""
    if days <= 0:
        raise ValueError("window must be at least one day")
    if conditional >= 1.0:
        return math.inf
    if conditional <= 0.0:
        return 0.0
    return -math.log(1.0 - conditional) / days


def monthly_equivalent(rate_per_day: float, days: int = 30) -> float:
    """The same hazard expressed as a probability over a standard 30-day month."""
    if math.isinf(rate_per_day):
        return 1.0
    return 1.0 - math.exp(-rate_per_day * days)


def build_curve(
    rungs: Iterable[Rung],
    *,
    today: date,
    min_window_days: int = MIN_INFORMATIVE_WINDOW_DAYS,
    as_of: str = "",
) -> HazardCurve:
    """Convert a cumulative ladder into comparable forward hazards.

    Short legs are computed and reported rather than silently dropped, so a reader can see
    what was excluded and why.
    """
    ordered = sorted(rungs, key=lambda r: r.resolves)
    curve = HazardCurve(as_of=as_of)
    previous_p = 0.0
    previous_d = today

    for rung in ordered:
        days = (rung.resolves - previous_d).days
        if days <= 0:
            # A rung at or before the anchor date carries no window to spread risk over.
            curve.points.append(
                HazardPoint(
                    label=rung.label,
                    resolves=rung.resolves.isoformat(),
                    window_days=days,
                    cumulative=rung.cumulative,
                    forward_conditional=0.0,
                    hazard_per_day=0.0,
                    monthly_equivalent=0.0,
                    informative=False,
                    excluded_because="window has already closed",
                )
            )
            curve.excluded.append(rung.label)
            previous_p, previous_d = rung.cumulative, rung.resolves
            continue

        conditional = forward_conditional(previous_p, rung.cumulative)
        rate = hazard_per_day(conditional, days)
        informative = days >= min_window_days
        reason = "" if informative else f"window of {days} days sits at the tick floor"
        curve.points.append(
            HazardPoint(
                label=rung.label,
                resolves=rung.resolves.isoformat(),
                window_days=days,
                cumulative=rung.cumulative,
                forward_conditional=conditional,
                hazard_per_day=rate,
                monthly_equivalent=monthly_equivalent(rate),
                informative=informative,
                excluded_because=reason,
            )
        )
        if not informative:
            curve.excluded.append(rung.label)
        previous_p, previous_d = rung.cumulative, rung.resolves

    return curve
