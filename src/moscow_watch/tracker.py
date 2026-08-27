"""Renders TRACKER.md.

The rule this file exists to enforce: **it renders no verdict, no score, no ranking and no
aggregate of any kind.** Every indicator gets a current value, when it was collected, when
it becomes decidable, and which hypotheses a move would bear on. If a reader wants to know
which hypothesis is winning, they read the article, where a named human says so.

The page opens with the resolution calendar, because what becomes decidable next is the
most useful thing a returning reader can be told.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from typing import Any

from .config import Config, Indicator
from .models import utc_now_iso


@dataclass(slots=True)
class Reading:
    """One indicator's current value, with the provenance needed to check it."""

    indicator_id: str
    name: str
    source: str
    kind: str
    value: float | None
    display: str
    collected_at: str
    resolves: str = ""
    unit: str = ""
    detail: str = ""
    source_url: str = ""
    available: bool = True
    unavailable_reason: str = ""
    components: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _fmt_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value * 100:.1f}%"


def _fmt_count(value: float | None) -> str:
    return "n/a" if value is None else f"{value:,.2f}".rstrip("0").rstrip(".")


def format_value(indicator: Indicator, value: float | None) -> str:
    if value is None:
        return "n/a"
    if indicator.kind in {"market_probability", "market_ladder"}:
        return _fmt_pct(value)
    return _fmt_count(value)


def _days_until(target: str, *, today: date) -> int | None:
    try:
        return (date.fromisoformat(target) - today).days
    except (TypeError, ValueError):
        return None


def resolution_calendar(
    config: Config, readings: Iterable[Reading], *, today: date
) -> list[dict[str, Any]]:
    """What becomes decidable next, soonest first.

    Includes both indicator resolution dates and the stated hypothesis falsifier dates,
    because the falsifiers are the commitments that make the tracker worth reading.
    """
    entries: dict[str, dict[str, Any]] = {}

    def add(when: str, what: str, bears_on: list[str], kind: str) -> None:
        if not when:
            return
        row = entries.setdefault(
            when, {"date": when, "days_away": _days_until(when, today=today), "items": []}
        )
        row["items"].append({"what": what, "bears_on": bears_on, "kind": kind})

    by_id = {i.id: i for i in config.enabled_indicators}
    for reading in readings:
        indicator = by_id.get(reading.indicator_id)
        if indicator is None or not indicator.resolves:
            continue
        add(
            indicator.resolves,
            indicator.name,
            sorted({b.hypothesis for b in indicator.bearings}),
            "indicator resolves",
        )
    for hypothesis in config.hypotheses:
        if hypothesis.scored and hypothesis.falsifier_date:
            add(
                hypothesis.falsifier_date,
                f"Falsifier for {hypothesis.id.upper()} ({hypothesis.name})",
                [hypothesis.id],
                "falsifier",
            )
    rows = sorted(entries.values(), key=lambda r: r["date"])
    return [r for r in rows if (r["days_away"] is None or r["days_away"] >= 0)]


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _bearing_text(indicator: Indicator) -> str:
    parts = []
    for bearing in indicator.bearings:
        arrow = {"up": "↑", "down": "↓", "flat": "→"}.get(bearing.direction, bearing.direction)
        parts.append(f"{bearing.hypothesis.upper()} {arrow}")
    return ", ".join(parts)


def render(
    config: Config,
    readings: list[Reading],
    *,
    health: dict[str, Any] | None = None,
    today: date | None = None,
) -> str:
    today = today or datetime.now(UTC).date()
    by_id = {i.id: i for i in config.enabled_indicators}
    summary = (health or {}).get("summary", {})

    lines = [
        "# Tracker",
        "",
        "_Generated. Do not edit by hand._",
        "",
        f"**Generated:** {utc_now_iso()}",
        "",
        "This page lists what was collected, from where, and when each thing becomes "
        "decidable. **It contains no verdict, no score and no ranking**, by design. Which "
        "hypothesis the evidence favours is a judgement, and judgements belong in the "
        "article with a name attached.",
        "",
        "Every value below was collected from the named source. Nothing here is a "
        "placeholder, an illustrative figure, or a default standing in for missing data. "
        "If a collector failed, its row says so.",
        "",
    ]

    # ---- Resolution calendar, first, because it is the most useful thing here ----
    calendar = resolution_calendar(config, readings, today=today)
    lines.extend(["## What resolves next", ""])
    if calendar:
        lines.extend(["| Date | Days away | What becomes decidable | Bears on |",
                      "| --- | ---: | --- | --- |"])
        for row in calendar[:12]:
            for item in row["items"]:
                bears = ", ".join(h.upper() for h in item["bears_on"]) or "—"
                what = (
                    f"**{item['what']}**" if item["kind"] == "falsifier" else item["what"]
                )
                lines.append(
                    f"| {row['date']} | {row['days_away'] if row['days_away'] is not None else '—'} "
                    f"| {_cell(what)} | {bears} |"
                )
    else:
        lines.append("No dated resolutions are configured.")
    lines.append("")

    # ---- Hypotheses and their falsifiers ----
    lines.extend([
        "## Hypotheses",
        "",
        "Each tracked hypothesis states, in advance, what would falsify it and by when. "
        "That commitment is the point; without it a tracker is just a feed.",
        "",
        "| | Hypothesis | Falsifier | By |",
        "| --- | --- | --- | --- |",
    ])
    for hypothesis in config.hypotheses:
        if not hypothesis.scored:
            continue
        lines.append(
            f"| **{hypothesis.id.upper()}** | {_cell(hypothesis.name)} | "
            f"{_cell(hypothesis.falsifier)} | {hypothesis.falsifier_date or '—'} |"
        )
    noted = [h for h in config.hypotheses if not h.scored]
    if noted:
        lines.append("")
        for hypothesis in noted:
            lines.append(
                f"**{hypothesis.id.upper()} — {hypothesis.name}: named and not tracked.** "
                f"{_cell(hypothesis.note)}"
            )
    lines.append("")

    # ---- Readings, grouped by source ----
    lines.extend(["## Indicators", ""])
    grouped: dict[str, list[Reading]] = defaultdict(list)
    for reading in readings:
        grouped[reading.source].append(reading)

    titles = {
        "polymarket": "Polymarket",
        "kalshi": "Kalshi",
        "portwatch": "IMF PortWatch (counted quantity)",
        "corpus": "Collected corpus",
        "gdelt": "GDELT reporting index (volume only — it attests nothing)",
    }
    for source in ("polymarket", "kalshi", "portwatch", "corpus", "gdelt"):
        rows = grouped.get(source, [])
        if not rows:
            continue
        lines.extend([f"### {titles.get(source, source)}", "",
                      "| Indicator | Value | Collected | Resolves | Bears on |",
                      "| --- | ---: | --- | --- | --- |"])
        for reading in sorted(rows, key=lambda r: r.name):
            indicator = by_id.get(reading.indicator_id)
            bearings = _bearing_text(indicator) if indicator else ""
            if reading.available:
                value = reading.display
            else:
                value = f"unavailable — {_cell(reading.unavailable_reason)[:60]}"
            link = f"[{_cell(reading.name)}]({reading.source_url})" if reading.source_url else _cell(reading.name)
            lines.append(
                f"| {link} | {value} | {reading.collected_at[:16] or '—'} | "
                f"{reading.resolves or '—'} | {bearings} |"
            )
        lines.append("")
        for reading in sorted(rows, key=lambda r: r.name):
            if reading.detail:
                lines.append(f"- **{_cell(reading.name)}** — {_cell(reading.detail)}")
        lines.append("")

    # ---- Notes that must travel with specific numbers ----
    notes = [(by_id[r.indicator_id].name, by_id[r.indicator_id].note)
             for r in readings if r.indicator_id in by_id and by_id[r.indicator_id].note]
    if notes:
        lines.extend(["## Notes attached to particular indicators", ""])
        for name, note in sorted(set(notes)):
            lines.append(f"- **{_cell(name)}** — {_cell(note)}")
        lines.append("")

    # ---- Source health ----
    lines.extend(["## Collection health", ""])
    if summary:
        layers = summary.get("layers", {})
        lines.extend(["| Layer | Healthy | Last success |", "| --- | --- | --- |"])
        for key, label in (
            ("polymarket", "Polymarket"),
            ("kalshi", "Kalshi"),
            ("portwatch", "IMF PortWatch"),
            ("independent_reporting", "Independent reporting"),
            ("primary_record", "Primary records"),
            ("discovery", "Discovery (GDELT, never promotes a claim)"),
            ("gdelt", "GDELT reporting index (volume only)"),
        ):
            layer = layers.get(key)
            if not layer:
                continue
            lines.append(
                f"| {label} | {layer.get('ok', 0)} of {layer.get('configured', 0)}"
                + (f", {layer['disabled']} disabled" if layer.get("disabled") else "")
                + f" | {layer.get('last_success_at') or 'never'} |"
            )
        lines.append("")
        failed = [
            s for s in (health or {}).get("sources", {}).values()
            if s.get("status") in {"failed", "disabled"}
        ]
        if failed:
            lines.extend(["| Source | Status | Detail |", "| --- | --- | --- |"])
            for item in sorted(failed, key=lambda s: str(s.get("source_id"))):
                lines.append(
                    f"| {_cell(item.get('label'))} | {item.get('status')} | "
                    f"{_cell(item.get('error_message', ''))[:150]} |"
                )
            lines.append("")
    else:
        lines.append("No collection has been recorded yet.")
        lines.append("")

    lines.extend([
        "---",
        "",
        "Rendered by `mw tracker`. Methodology: [docs/METHODOLOGY.md](docs/METHODOLOGY.md). "
        "Sources and their terms: [docs/SOURCES.md](docs/SOURCES.md).",
    ])
    return "\n".join(lines) + "\n"
