"""Renders CHANGES.md — what moved since a chosen point.

This is the feature the follow-up articles are written from, so it is treated as the
primary deliverable of the codebase. A follow-up should start from a generated changelog,
not from a blank page.

Two suppressions keep it honest, and both matter more than they sound:

- **No move computed over a window shorter than `min_change_window_hours`.** An earlier
  version of this project reported half-point moves over three-minute windows. It made
  noise look like news and it discredited the whole page.
- **No move smaller than the indicator's own `material_move`**, which is fixed in advance
  in `indicators.toml` rather than chosen after seeing the data.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from typing import Any

from .config import Config, Indicator
from .models import parse_time, utc_now_iso
from .tracker import format_value


@dataclass(slots=True)
class Movement:
    indicator_id: str
    name: str
    source: str
    before: float | None
    after: float | None
    change: float
    before_at: str
    after_at: str
    window_hours: float
    material_move: float
    display_before: str
    display_after: str
    display_change: str
    bears_on: list[dict[str, str]] = field(default_factory=list)
    resolves: str = ""
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _hours_between(earlier: str, later: str) -> float | None:
    try:
        return (parse_time(later) - parse_time(earlier)).total_seconds() / 3600.0
    except (TypeError, ValueError):
        return None


def _series_for(rows: Iterable[dict[str, Any]], indicator_id: str) -> list[dict[str, Any]]:
    series = [r for r in rows if str(r.get("indicator_id")) == indicator_id and r.get("available", True)]
    series.sort(key=lambda r: str(r.get("collected_at", "")))
    return series


def find_movements(
    config: Config,
    history: list[dict[str, Any]],
    *,
    since: str,
    min_window_hours: float | None = None,
) -> list[Movement]:
    """Movements that clear both the time window and the indicator's own threshold."""
    min_window = (
        config.min_change_window_hours if min_window_hours is None else min_window_hours
    )
    movements: list[Movement] = []

    for indicator in config.enabled_indicators:
        series = _series_for(history, indicator.id)
        if len(series) < 2:
            continue
        latest = series[-1]
        # The earliest reading at or after `since`; falls back to the oldest we hold.
        baseline = next(
            (r for r in series if str(r.get("collected_at", "")) >= since), series[0]
        )
        if baseline is latest or baseline.get("collected_at") == latest.get("collected_at"):
            continue

        before = baseline.get("value")
        after = latest.get("value")
        if before is None or after is None:
            continue

        window = _hours_between(str(baseline["collected_at"]), str(latest["collected_at"]))
        if window is None or window < min_window:
            # Too short a window to distinguish a move from noise.
            continue

        change = float(after) - float(before)
        if abs(change) < indicator.material_move:
            continue

        movements.append(
            Movement(
                indicator_id=indicator.id,
                name=indicator.name,
                source=indicator.source,
                before=float(before),
                after=float(after),
                change=round(change, 6),
                before_at=str(baseline["collected_at"]),
                after_at=str(latest["collected_at"]),
                window_hours=round(window, 2),
                material_move=indicator.material_move,
                display_before=format_value(indicator, float(before)),
                display_after=format_value(indicator, float(after)),
                display_change=_display_change(indicator, change),
                bears_on=list(indicator.bears_on),
                resolves=indicator.resolves,
                note=indicator.note,
            )
        )

    movements.sort(key=lambda m: abs(m.change), reverse=True)
    return movements


def _display_change(indicator: Indicator, change: float) -> str:
    if indicator.kind in {"market_probability", "market_ladder"}:
        return f"{change * 100:+.1f} pts"
    return f"{change:+,.2f}".rstrip("0").rstrip(".")


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _bearing_text(bears_on: list[dict[str, str]], change: float) -> str:
    """Which hypotheses this particular move points toward, given its direction."""
    moved = "up" if change > 0 else "down"
    pointing = [b["hypothesis"].upper() for b in bears_on if b.get("direction") == moved]
    against = [b["hypothesis"].upper() for b in bears_on if b.get("direction") not in (moved, None)]
    parts = []
    if pointing:
        parts.append("toward " + ", ".join(sorted(pointing)))
    if against:
        parts.append("away from " + ", ".join(sorted(against)))
    return "; ".join(parts) or "—"


def render(
    config: Config,
    movements: list[Movement],
    *,
    since: str,
    rules_changes: list[dict[str, Any]] | None = None,
    suppressed: int = 0,
) -> str:
    rules_changes = rules_changes or []
    lines = [
        "# Changes",
        "",
        "_Generated. Do not edit by hand._",
        "",
        f"**Generated:** {utc_now_iso()}  ",
        f"**Since:** {since}",
        "",
        "Everything below cleared two thresholds fixed in advance: a minimum observation "
        f"window of {config.min_change_window_hours:g} hours, and the indicator's own "
        "`material_move`. Smaller or faster wobbles are not reported, because they are "
        "noise and reporting them as news is how a tracker loses its reader.",
        "",
        "A move is not evidence for a hypothesis. It is a change in a number that would "
        "*bear on* one, in a direction stated before the move happened.",
        "",
    ]

    lines.extend(["## Indicators that moved", ""])
    if movements:
        lines.extend([
            "| Indicator | Then | Now | Move | Window | Points |",
            "| --- | ---: | ---: | ---: | ---: | --- |",
        ])
        for m in movements:
            lines.append(
                f"| {_cell(m.name)} | {m.display_before} | {m.display_after} | "
                f"{m.display_change} | {m.window_hours:.0f} h | "
                f"{_bearing_text(m.bears_on, m.change)} |"
            )
        lines.append("")
        for m in movements:
            if m.note:
                lines.append(f"- **{_cell(m.name)}** — {_cell(m.note)}")
        lines.append("")
    else:
        lines.append(
            "No indicator moved beyond its threshold in this window. That is a result, "
            "not a failure: most weeks nothing happens, and a tracker that manufactures "
            "movement to fill a page is worse than one that says so."
        )
        lines.append("")

    if suppressed:
        lines.extend([
            f"_{suppressed} smaller move(s) were observed and deliberately not reported, "
            "having failed the window or threshold test._",
            "",
        ])

    lines.extend(["## Resolution wording and new markets", ""])
    if rules_changes:
        lines.append(
            "A change to resolution wording is a material event: the same ticker can "
            "silently start meaning something different, and a chart plotted straight "
            "through such a change is misleading."
        )
        lines.append("")
        new = [c for c in rules_changes if c.get("kind") == "new_market"]
        changed = [c for c in rules_changes if c.get("kind") == "rules_changed"]
        if changed:
            lines.extend(["### Resolution wording changed", ""])
            for c in changed:
                lines.append(f"**{_cell(c.get('ticker'))}** — {_cell(c.get('title'))}")
                lines.append("")
                lines.append(f"- Before: {_cell(c.get('before', ''))[:300]}")
                lines.append(f"- After: {_cell(c.get('after', ''))[:300]}")
                if c.get("settlement_sources_before") != c.get("settlement_sources_after"):
                    lines.append(
                        f"- Settlement sources: {_cell(c.get('settlement_sources_before'))} "
                        f"→ {_cell(c.get('settlement_sources_after'))}"
                    )
                lines.append("")
        if new:
            lines.extend(["### New markets listed in a tracked series", "",
                          "| Ticker | Title | Closes |", "| --- | --- | --- |"])
            for c in new:
                lines.append(
                    f"| {_cell(c.get('ticker'))} | {_cell(c.get('title'))} | "
                    f"{str(c.get('close_time', ''))[:10]} |"
                )
            lines.append("")
    else:
        lines.append("No resolution wording changed and no new markets appeared in a tracked series.")
        lines.append("")

    lines.extend([
        "---",
        "",
        "Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).",
    ])
    return "\n".join(lines) + "\n"


def count_suppressed(
    config: Config, history: list[dict[str, Any]], *, since: str
) -> int:
    """How many real moves were withheld, so the suppression is visible rather than silent."""
    suppressed = 0
    for indicator in config.enabled_indicators:
        series = _series_for(history, indicator.id)
        if len(series) < 2:
            continue
        latest = series[-1]
        baseline = next(
            (r for r in series if str(r.get("collected_at", "")) >= since), series[0]
        )
        before, after = baseline.get("value"), latest.get("value")
        if before is None or after is None or baseline is latest:
            continue
        window = _hours_between(str(baseline["collected_at"]), str(latest["collected_at"]))
        change = abs(float(after) - float(before))
        if change == 0:
            continue
        if window is None or window < config.min_change_window_hours or change < indicator.material_move:
            suppressed += 1
    return suppressed
