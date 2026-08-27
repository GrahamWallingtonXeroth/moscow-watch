"""Russia–Iran engagement volume: fortnight buckets, baseline, direction.

The discriminator map needs one thing the directly collected contact counter cannot give
it: a reading from *before* 25 August 2026. RSS exposes a few days, so the counter starts
at first run and has nothing behind it. A news index does hold history, and this module
turns that history into the baseline the horizontal axis is measured against.

What that buys, and what it costs, stated once and repeated wherever the number appears:

1. This is **reporting volume**, not a count of contacts. The value is the share of the
   coverage GDELT monitored that day which matched the query. It is a proxy for
   diplomatic tempo, not a tally of meetings.
2. Because it is a share of coverage, **only the direction of change against the baseline
   is meaningful**. The level on its own says nothing, and no level is ever published as
   though it did.
3. Counting how much a subject is reported and attesting that something happened are
   different operations. Nothing here attests anything, promotes anything, or corroborates
   anything. The directly collected contact counter, with a citation behind every entry,
   remains the auditable series.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date, timedelta
from typing import Any

from .collectors.contacts import fortnight_start


def fortnightly_volume(
    points: Iterable[dict[str, Any]], *, anchor: date, since: date | None = None
) -> list[dict[str, Any]]:
    """Mean daily volume per fortnight, bucketed in 14-day windows from `anchor`.

    The baseline is bucketed from the counter's anchor and the live series from the event
    date, because a window straddling 25 August would average the days before the visit
    together with the days after it and answer a different question from the one asked.
    Both are 14-day windows of the same daily quantity, so their means are comparable.
    """
    buckets: dict[date, list[float]] = {}
    for row in points:
        try:
            day = date.fromisoformat(str(row.get("day"))[:10])
            value = float(row.get("value"))
        except (TypeError, ValueError):
            continue
        if since is not None and day < since:
            continue
        buckets.setdefault(fortnight_start(day, anchor=anchor), []).append(value)

    series: list[dict[str, Any]] = []
    for start in sorted(buckets):
        values = buckets[start]
        series.append(
            {
                "fortnight_start": start.isoformat(),
                "fortnight_end": (start + timedelta(days=13)).isoformat(),
                "mean_volume": round(sum(values) / len(values), 5),
                "max_volume": round(max(values), 5),
                "days": len(values),
            }
        )
    return series


def baseline(series: Iterable[dict[str, Any]], *, before: date) -> dict[str, Any]:
    """Pre-event baseline, so 'up' or 'down' is measured against something stated.

    Only whole fortnights that end before the event are used. A bucket straddling the
    event date contains the event's own coverage spike and would flatter the baseline.
    """
    prior = []
    for bucket in series:
        try:
            end = date.fromisoformat(str(bucket["fortnight_end"]))
        except (KeyError, TypeError, ValueError):
            continue
        if end < before:
            prior.append(float(bucket.get("mean_volume") or 0.0))
    if not prior:
        return {"fortnights": 0, "mean_volume": None, "before": before.isoformat()}
    return {
        "fortnights": len(prior),
        "mean_volume": round(sum(prior) / len(prior), 5),
        "max_volume": round(max(prior), 5),
        "before": before.isoformat(),
    }


def direction(
    series: list[dict[str, Any]], base: dict[str, Any], *, tolerance: float = 0.10
) -> str:
    """down / flat / up against the stated baseline, or 'insufficient data'.

    `tolerance` is a fraction of the baseline, because the level is arbitrary and only a
    relative move means anything. Deliberately coarse: a finer reading than a coverage
    share supports would be false precision.
    """
    mean = base.get("mean_volume")
    if mean is None or not series:
        return "insufficient data"
    try:
        latest = float(series[-1].get("mean_volume"))
    except (TypeError, ValueError):
        return "insufficient data"
    if mean <= 0:
        return "insufficient data"
    if latest > mean * (1 + tolerance):
        return "up"
    if latest < mean * (1 - tolerance):
        return "down"
    return "flat"


# Half a fortnight. The baseline is built from whole fortnights, so a bucket with two days
# in it is not a comparable quantity however tempting the number looks. Below this the
# marker is left undrawn, which is the honest reading of a series that has just started.
MIN_DAYS_TO_PLACE_MARKER = 7


def axis_position(series: list[dict[str, Any]], base: dict[str, Any]) -> float | None:
    """The discriminator map's horizontal axis: −1 pulls back … +1 leans in.

    Returns None when the baseline is missing or the current fortnight is too thin, so the
    marker is left undrawn rather than guessed.
    """
    mean = base.get("mean_volume")
    if mean is None or mean <= 0 or not series:
        return None
    latest = series[-1]
    if int(latest.get("days") or 0) < MIN_DAYS_TO_PLACE_MARKER:
        return None
    try:
        value = float(latest.get("mean_volume"))
    except (TypeError, ValueError):
        return None
    return max(-1.0, min(1.0, (value - mean) / mean))
