"""Generate the Moscow Watch graphics.

Three figures, regenerated on every collection run:

  discriminator-map.png  the six hypotheses on two measured axes, with the
                         current position of the story marked from live data
  hazard-curve.png       the Polymarket Russia-Ukraine ceasefire ladder,
                         converted to forward conditional hazard rates
  hero-sequence.png      the established sequence of 17-26 August

Both read from data/latest.json in production. The defaults below are the
verified readings for 26 August 2026 so the module runs standalone.
"""
from __future__ import annotations

import math
from datetime import date

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

INK        = "#0E1116"
PANEL      = "#171B22"
GRID       = "#2A313C"
TEXT       = "#E8EAED"
MUTED      = "#8B94A3"
FAINT      = "#5A6472"
ACCENT     = "#E4B363"   # the finding
LIVE       = "#4EA1D3"   # live position
WARN       = "#D96C6C"

FAMILY = ["DejaVu Sans"]

plt.rcParams.update({
    "font.family": FAMILY,
    "figure.facecolor": INK,
    "savefig.facecolor": INK,
    "text.color": TEXT,
    "axes.facecolor": INK,
    "axes.edgecolor": GRID,
    "axes.labelcolor": MUTED,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
})


# --------------------------------------------------------------------------
# Figure 1: the discriminator map
# --------------------------------------------------------------------------

CELLS = {
    # (col, row): (tag, name, blurb)
    (0, 2): ("H3", "Bargain",   "US gives ground in Ukraine;\nMoscow drops Iran"),
    (1, 2): ("H2", "Ukraine",   "Settlement groundwork\nthe envoys could not lay"),
    (2, 2): ("H1", "Custody",   "A route for 440kg\nof missing uranium"),
    (1, 1): ("H6", "Routine",   "Prisoners, channel,\nembassy business"),
    (2, 1): ("H4", "Brokerage", "Moscow carries a message\nto post-Khamenei Tehran"),
    (0, 0): ("H5", "Warning",   "Stop giving Iran\ntargeting data on US ships"),
}

COLS = ["Russia pulls back\nfrom Tehran", "No change", "Russia leans in\nto Tehran"]
ROWS = ["Washington\nimposes costs", "No change", "Washington\noffers relief"]


def discriminator_map(position=None, as_of="26 August 2026", path="discriminator-map.png",
                      note=""):
    """`position` of None means the ledger could not place the marker.

    In that case the marker is drawn at centre and labelled "not yet determined", rather
    than guessed. Where the marker sits must always be derivable from the ledger.
    """
    fig, ax = plt.subplots(figsize=(16, 11), dpi=100)
    ax.set_xlim(-1.62, 2.62)
    ax.set_ylim(-1.18, 3.30)
    ax.axis("off")

    fig.text(0.052, 0.960, "Why did the CIA director fly to Moscow?",
             fontsize=34, fontweight="bold", color=TEXT, va="top")
    fig.text(0.052, 0.903,
             "Six explanations. Two quantities we can actually count. The marker moves as the data does.",
             fontsize=17.5, color=MUTED, va="top")

    for (col, row), (tag, name, blurb) in CELLS.items():
        ax.add_patch(FancyBboxPatch(
            (col - 0.43, row - 0.38), 0.86, 0.76,
            boxstyle="round,pad=0.016,rounding_size=0.035",
            linewidth=1.4, edgecolor=GRID, facecolor=PANEL, zorder=2))
        ax.text(col - 0.36, row + 0.25, tag, fontsize=13.5, color=FAINT,
                fontweight="bold", va="center", zorder=3)
        ax.text(col - 0.36, row + 0.08, name, fontsize=21, color=TEXT,
                fontweight="bold", va="center", zorder=3)
        ax.text(col - 0.36, row - 0.20, blurb, fontsize=13, color=MUTED,
                va="center", linespacing=1.55, zorder=3)

    for (col, row) in [(0, 1), (1, 0), (2, 0)]:
        ax.add_patch(FancyBboxPatch(
            (col - 0.43, row - 0.38), 0.86, 0.76,
            boxstyle="round,pad=0.016,rounding_size=0.035",
            linewidth=1.1, edgecolor="#20262E", facecolor="#12161C",
            linestyle=(0, (4, 4)), zorder=1))
        ax.text(col, row, "no coherent\nexplanation", fontsize=12.5, color="#3D4552",
                ha="center", va="center", style="italic", linespacing=1.6, zorder=2)

    for i, label in enumerate(COLS):
        ax.text(i, 2.72, label, fontsize=15.5, color=TEXT, ha="center",
                va="center", fontweight="bold", linespacing=1.5)
    ax.text(1.0, 3.14, " ".join("WHICH WAY ARE RUSSIAN OFFICIALS TRAVELLING?"),
            fontsize=13, color=ACCENT, ha="center", va="center", fontweight="bold")

    for i, label in enumerate(ROWS):
        ax.text(-0.90, i, label, fontsize=15.5, color=TEXT, ha="right",
                va="center", fontweight="bold", linespacing=1.5)
    ax.text(-1.52, 1.0, " ".join("WHAT WASHINGTON DOES TO RUSSIA"),
            fontsize=11.5, color=ACCENT, ha="center", va="center",
            fontweight="bold", rotation=90)

    determined = position is not None
    x, y = position if determined else (1.0, 1.0)
    if determined:
        for r, a in ((0.26, 0.11), (0.185, 0.18), (0.12, 0.28)):
            ax.add_patch(Circle((x, y), r, facecolor=LIVE, alpha=a, edgecolor="none", zorder=4))
        ax.add_patch(Circle((x, y), 0.062, facecolor=LIVE, edgecolor=INK, linewidth=2.4,
                            zorder=5))
    else:
        # A filled marker parked at centre reads as "the answer is the middle cell".
        # An empty ring, drawn behind the cells, reads as "nothing placed here yet".
        ax.add_patch(Circle((x, y), 0.30, facecolor="none", edgecolor=LIVE, alpha=0.45,
                            linewidth=2.0, linestyle=(0, (5, 4)), zorder=1))
    ax.plot([x, 1.50, 1.50, -0.30], [y, y, -0.66, -0.66], color=LIVE,
            linewidth=1.3, alpha=0.75 if determined else 0.35, zorder=1,
            solid_capstyle="round")
    headline = (
        f"Where the evidence sits, {as_of}:" if determined
        else f"Not yet determined, {as_of}:"
    )
    detail = (
        note or "no confirmed shift in either direction. Everything above is still open."
        if determined
        else "not enough collected data to place the marker. It is centred, not inferred."
    )
    ax.text(-0.40, -0.66, headline, fontsize=14.5,
            color=LIVE, fontweight="bold", ha="right", va="center", zorder=6)
    ax.text(-0.40, -0.94, detail,
            fontsize=13.5, color=MUTED, ha="right", va="center", zorder=6)

    fig.text(0.052, 0.043,
             "Live tracker  ·  github.com/GrahamWallingtonXeroth/moscow-watch",
             fontsize=13.5, color=FAINT)
    fig.text(0.948, 0.043,
             "Sources: Polymarket · Kalshi · IMF PortWatch · official readouts",
             fontsize=13.5, color=FAINT, ha="right")

    fig.savefig(path, bbox_inches="tight", pad_inches=0.40, facecolor=INK)
    plt.close(fig)
    return path


# --------------------------------------------------------------------------
# Figure 2: the hazard curve
# --------------------------------------------------------------------------

LADDER = [
    ("31 Aug\n2026",  date(2026, 8, 31), 0.019),
    ("31 Oct\n2026",  date(2026, 10, 31), 0.115),
    ("31 Dec\n2026",  date(2026, 12, 31), 0.250),
    ("31 Mar\n2027",  date(2027, 3, 31),  0.440),
    ("30 Jun\n2027",  date(2027, 6, 30),  0.535),
]


def hazard_curve(ladder=LADDER, today=date(2026, 8, 26), as_of="26 August 2026",
                 min_window_days=14, path="hazard-curve.png"):
    """Legs shorter than `min_window_days` sit at the exchange tick floor and carry no
    information; they are computed, excluded from the plot, and the exclusion is stated."""
    labels, monthly, dropped = [], [], []
    prev_p, prev_d = 0.0, today
    for name, d, p in ladder:
        days = (d - prev_d).days
        cond = (p - prev_p) / (1 - prev_p)
        lam = -math.log(max(1e-9, 1 - cond)) / days
        if days < min_window_days:
            dropped.append(name.replace("\n", " "))
        else:
            labels.append(name)
            monthly.append((1 - math.exp(-lam * 30)) * 100)
        prev_p, prev_d = p, d

    fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
    fig.subplots_adjust(left=0.095, right=0.955, top=0.735, bottom=0.175)

    fig.text(0.095, 0.958, "The market does not think a Ukraine deal is close",
             fontsize=33, fontweight="bold", color=TEXT, va="top")
    fig.text(0.095, 0.888,
             "Polymarket's ceasefire ladder, converted to the monthly chance of a deal arriving in each window.\n"
             "Raw prices climb with time simply because the window is longer. This strips that out.",
             fontsize=16.5, color=MUTED, va="top", linespacing=1.7)

    x = list(range(len(labels)))
    peak = max(x, key=lambda i: monthly[i])
    trough = min(x, key=lambda i: monthly[i])

    ax.axvspan(peak - 0.46, peak + 0.46, color=ACCENT, alpha=0.075, zorder=0)
    ax.bar(x, monthly, width=0.54, zorder=3, edgecolor="none",
           color=[ACCENT if i == peak else "#33404F" for i in x])
    ax.plot(x, monthly, color=TEXT, linewidth=2.0, alpha=0.28, zorder=4,
            marker="o", markersize=6, markerfacecolor=INK, markeredgewidth=1.6)

    for i, v in enumerate(monthly):
        ax.text(i, v + 0.30, f"{v:.1f}%", ha="center", fontsize=19,
                fontweight="bold", color=ACCENT if i == peak else TEXT, zorder=5)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=16, color=TEXT, linespacing=1.5)
    ax.set_ylabel("Monthly chance of a ceasefire\nagreement arriving in that window",
                  fontsize=14, color=MUTED, labelpad=18, linespacing=1.7)
    ax.set_ylim(0, max(monthly) * 1.42)
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.5, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)

    ax.annotate("The modal deal window is\nthe first quarter of 2027",
                xy=(peak - 0.30, monthly[peak] + 0.55),
                xytext=(peak - 1.62, max(monthly) * 1.30),
                fontsize=17, color=ACCENT, fontweight="bold", linespacing=1.55,
                va="top",
                arrowprops=dict(arrowstyle="->", color=ACCENT, linewidth=1.8,
                                connectionstyle="arc3,rad=-0.20"))
    ax.annotate("Least likely window:\nthe next two months",
                xy=(trough, monthly[trough] + 0.30),
                xytext=(trough + 0.34, max(monthly) * 0.30),
                fontsize=14.5, color=MUTED, linespacing=1.55,
                arrowprops=dict(arrowstyle="->", color=FAINT, linewidth=1.3,
                                connectionstyle="arc3,rad=-0.30"))

    note = ("Polymarket 'Russia x Ukraine ceasefire agreement by' ladder, " + as_of +
            ". Forward conditional hazard between adjacent legs.")
    if dropped:
        note += "  The " + ", ".join(dropped) + " leg sits at the tick floor and is excluded."
    fig.text(0.095, 0.055, note, fontsize=12.5, color=FAINT)
    fig.text(0.095, 0.022, "github.com/GrahamWallingtonXeroth/moscow-watch",
             fontsize=12.5, color=FAINT)

    fig.savefig(path, bbox_inches="tight", pad_inches=0.40, facecolor=INK)
    plt.close(fig)
    return path


if __name__ == "__main__":
    print(discriminator_map())
    print(hazard_curve())


# ---------------------------------------------------------------------------
# Data wiring.
#
# Everything below reads the collected ledgers. Neither chart may take a position
# from a literal: if the ledger cannot support a marker, the marker is not drawn.
# ---------------------------------------------------------------------------

from datetime import UTC, datetime  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Any  # noqa: E402


def _latest_legs(store, event_slug: str) -> list[dict[str, Any]]:
    """The most recent capture of every open leg of one event."""
    rows = [r for r in store.read("polymarket_legs") if r.get("event_slug") == event_slug]
    if not rows:
        return []
    newest = max(str(r.get("captured_at", "")) for r in rows)
    today = datetime.now(UTC).date()
    live: list[dict[str, Any]] = []
    for row in rows:
        if str(row.get("captured_at", "")) != newest:
            continue
        if row.get("closed") is True or row.get("archived") is True or row.get("active") is False:
            continue
        end = str(row.get("end_date") or "")[:10]
        try:
            if end and date.fromisoformat(end) <= today:
                continue
        except ValueError:
            continue
        if row.get("yes_price") is None:
            continue
        live.append(row)
    live.sort(key=lambda r: str(r.get("end_date", "")))
    return live


def ladder_from_store(store, event_slug: str):
    """Build hazard rungs from collected legs. Returns [] when the ledger has none."""
    from .hazard import Rung

    rungs = []
    for row in _latest_legs(store, event_slug):
        end = str(row.get("end_date") or "")[:10]
        try:
            resolves = date.fromisoformat(end)
        except ValueError:
            continue
        label = str(row.get("group_item_title") or end)
        rungs.append(
            Rung(
                label=label.replace(", ", "\n"),
                resolves=resolves,
                cumulative=float(row["yes_price"]),
                source="polymarket",
                ticker=str(row.get("market_slug", "")),
            )
        )
    return rungs


def us_posture_index(store, config) -> tuple[float | None, str]:
    """Y-axis: costs (-1) … relief (+1), from collected market prices only.

    Built from the two sanctions markets and the Ukraine security-guarantee market. Higher
    sanctions odds and higher guarantee odds both mean Washington is imposing costs, so the
    index is their mean, negated. The formula is stated in docs/METHODOLOGY.md so a reader
    can recompute the marker from the ledger.
    """
    wanted = {
        "kalshi_sanction_russia": 1.0,
        "kalshi_house_russia_sanction": 1.0,
        "pm_ukraine_security_guarantee": 1.0,
    }
    latest: dict[str, float] = {}
    for row in store.read("readings"):
        key = str(row.get("indicator_id"))
        if key in wanted and row.get("available", True) and row.get("value") is not None:
            if key not in latest or str(row.get("collected_at", "")) >= latest.get(f"{key}__at", ""):
                latest[key] = float(row["value"])
                latest[f"{key}__at"] = str(row.get("collected_at", ""))
    values = [latest[k] for k in wanted if k in latest]
    if len(values) < 2:
        return None, f"only {len(values)} of {len(wanted)} posture inputs collected"
    mean = sum(values) / len(values)
    # Centre on 0.5 and negate: more cost-imposition sits lower on the axis.
    return max(-1.0, min(1.0, -(mean - 0.5) * 2.0)), f"mean of {len(values)} market(s)"


def contact_axis(store, config) -> tuple[float | None, str]:
    """X-axis: Russia pulls back (-1) … Russia leans in (+1), from the contact counter."""
    series = sorted(store.read("contact_series"), key=lambda r: str(r.get("fortnight_start", "")))
    if not series:
        return None, "no contact series collected"
    from .collectors.contacts import baseline as contact_baseline

    base = contact_baseline(series, before=config.event_date)
    mean = base.get("mean_per_fortnight")
    if mean is None:
        return None, "no pre-event baseline available"
    latest = float(series[-1].get("count", 0))
    if mean == 0:
        return (0.0 if latest == 0 else 1.0), "baseline is zero"
    ratio = (latest - mean) / max(mean, 1.0)
    return max(-1.0, min(1.0, ratio)), f"latest {latest:.0f} vs baseline {mean:.2f}/fortnight"


# --------------------------------------------------------------------------
# Figure 3: the hero. Fixed sequence of established facts, not ledger data,
# so it is regenerated for consistency rather than because it can change.
# --------------------------------------------------------------------------

EVENTS = [
    (0, "above", "Aug 17",        "Talks to recover Iran's\nuranium expire. No deal."),
    (1, "below", "Aug 23",        "Ratcliffe leaves Washington\nfor Riga"),
    (2, "above", "Aug 25, 10.00", "C-17 lands at Vnukovo"),
    (3, "below", "Aug 25, 17.30", "Departs. No meeting\nwith Putin."),
    (4, "above", "Aug 26, 02.00", "Ten drones downed\nover Moscow"),
]


def hero_timeline(path="hero-sequence.png"):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
    fig.subplots_adjust(left=0.05, right=0.97, top=0.685, bottom=0.185)

    fig.text(0.05, 0.960, "Seven hours in Moscow", fontsize=46,
             fontweight="bold", color=TEXT, va="top")
    fig.text(0.05, 0.852,
             "What America's spy chief did between the collapse of the Iran talks\n"
             "and the drones returning over the Kremlin.",
             fontsize=19.5, color=MUTED, va="top", linespacing=1.7)

    ax.set_xlim(-0.62, 4.62)
    ax.set_ylim(-1.42, 1.62)
    ax.axis("off")

    ax.axvspan(1.50, 4.42, ymin=0.0, ymax=0.80, color=WARN, alpha=0.075, zorder=0)
    ax.text(2.96, -1.30, "Ukraine pauses strikes on Moscow and St Petersburg",
            fontsize=13.5, color="#B06565", ha="center", va="center",
            style="italic", zorder=2)

    ax.axhline(0, color=GRID, linewidth=1.6, zorder=1)

    ax.plot([0.30, 0.70], [0, 0], color=INK, linewidth=7, zorder=2)
    ax.text(0.50, 0.13, "eight days", fontsize=12.5, color=FAINT,
            ha="center", va="bottom", style="italic", zorder=3)

    ax.plot([2, 3], [1.14, 1.14], color=ACCENT, linewidth=1.6, zorder=3)
    ax.plot([2, 2], [1.05, 1.14], color=ACCENT, linewidth=1.6, zorder=3)
    ax.plot([3, 3], [1.05, 1.14], color=ACCENT, linewidth=1.6, zorder=3)
    ax.text(2.5, 1.22, "seven hours on the ground", fontsize=15,
            color=ACCENT, fontweight="bold", ha="center", va="bottom", zorder=4)

    for pos, side, stamp, text in EVENTS:
        up = side == "above"
        hot = pos in (2, 3)
        stem = 0.40 if up else -0.40
        ax.plot([pos, pos], [0, stem], color=FAINT, linewidth=1.3, zorder=2)
        ax.add_patch(Circle((pos, 0), 0.052, facecolor=ACCENT if hot else TEXT,
                            edgecolor=INK, linewidth=2.4, zorder=5))
        ax.text(pos, stem + (0.13 if up else -0.13), stamp, fontsize=15,
                color=ACCENT if hot else TEXT, fontweight="bold",
                ha="center", va="bottom" if up else "top", zorder=6)
        ax.text(pos, stem + (0.36 if up else -0.36), text, fontsize=13.5,
                color=MUTED, ha="center", va="bottom" if up else "top",
                linespacing=1.6, zorder=6)

    fig.text(0.05, 0.088,
             "440.9 kg of uranium enriched to 60% was last verified by the IAEA in June 2025.\n"
             "The agency says it can no longer account for its size, composition or whereabouts.",
             fontsize=16, color="#C9CDD4", va="top", linespacing=1.7)
    fig.text(0.97, 0.088,
             "Six explanations. One live tracker.\ngithub.com/GrahamWallingtonXeroth/moscow-watch",
             fontsize=13, color=FAINT, va="top", ha="right", linespacing=1.7)

    fig.savefig(path, bbox_inches="tight", pad_inches=0.42, facecolor=INK)
    plt.close(fig)
    return path


def render_all(config, store, out_dir: Path = Path("assets")) -> list[str]:
    """Regenerate both PNGs from the ledger. Committed on every run."""
    out_dir.mkdir(parents=True, exist_ok=True)
    as_of = datetime.now(UTC).strftime("%d %B %Y")
    written: list[str] = []

    rungs = ladder_from_store(store, "russia-x-ukraine-ceasefire-agreement-by")
    if rungs:
        ladder = [(r.label, r.resolves, r.cumulative) for r in rungs]
        written.append(
            hazard_curve(
                ladder=ladder,
                today=datetime.now(UTC).date(),
                as_of=as_of,
                path=str(out_dir / "hazard-curve.png"),
            )
        )
    else:
        print("hazard-curve.png skipped: no ceasefire ladder in the ledger")

    x, x_note = contact_axis(store, config)
    y, y_note = us_posture_index(store, config)
    if x is None or y is None:
        # Never guess a position. Centre it and say so.
        written.append(
            discriminator_map(
                position=None,
                as_of=as_of,
                path=str(out_dir / "discriminator-map.png"),
            )
        )
        print(f"discriminator marker not determined: x={x_note}; y={y_note}")
    else:
        written.append(
            discriminator_map(
                position=(1 + x, 1 + y),
                as_of=as_of,
                path=str(out_dir / "discriminator-map.png"),
            )
        )
    written.append(hero_timeline(path=str(out_dir / "hero-sequence.png")))
    return written
