# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-09-07T21:33:38Z
**Since:** 2026-08-31T21:33:38Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 5 | 4.29 | -0.71 | 167 h | away from H1, H4 |
| Kalshi: new US sanctions on Russia — KXSANCTIONRUSSIA-26JUL-NOV | kalshi:KXSANCTIONRUSSIA-26JUL-NOV | 2026-11-01T15:00:00Z | 41.0% | 12.0% | -29.0 pts | 167 h | toward H3; away from H5 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-NOV01 | kalshi:KXKASHRUSSIA-26JUL27-NOV01 | 2026-11-01T15:00:00Z | 61.0% | 42.0% | -19.0 pts | 167 h | away from H6 |
| Kalshi: Zelensky-Putin meeting — KXZELENSKYPUTIN-29-27 | kalshi:KXZELENSKYPUTIN-29-27 | 2027-01-01T04:59:00Z | 8.0% | 15.0% | +7.0 pts | 167 h | toward H2 |
| Polymarket: NATO-Russia military clash — October 31 | polymarket:nato-x-russia-military-clash-by-october-31-2026 | 2026-11-01T03:59:00Z | 13.5% | 7.5% | -6.0 pts | 167 h | away from H5 |
| Kalshi: Putin-Trump meeting location — KXPUTINDJTLOCATION-29-HUN | kalshi:KXPUTINDJTLOCATION-29-HUN | 2029-01-01T04:59:00Z | 5.0% | 10.0% | +5.0 pts | 167 h | toward H2 |
| Polymarket: Russia-Ukraine ceasefire term structure — December 31 | polymarket:russia-x-ukraine-ceasefire-agreement-by-december-31-2026 | 2027-01-01T04:59:00Z | 19.5% | 23.5% | +4.0 pts | 167 h | toward H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Kalshi: new US sanctions on Russia** — A US-posture input. Costs point to H5 and against the American leg of H3.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.

_15 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### Resolution wording changed

**KXWITKOFFRUSSIA-26JUN29-OCT01** — Will Steve Witkoff visit Russia before Oct 1, 2026?

- Secondary rule before: Physical presence within the geographic boundaries of the area is required. Flying over without landing, layovers during which the person remains in the airplane or airport, virtual or remote appearances, future visit plans, or (unless explicitly specified) presence in adjacent international waters
- Secondary rule after: The following do NOT constitute a visit:  Flying over the area without landing Layovers during which the person remains in an airplane Virtual or remote appearances Presence in international waters adjacent to the area Presence solely within embassy or consulate grounds Plans, announcements, or sche

**KXWITKOFFRUSSIA-26JUN29-JAN01** — Will Steve Witkoff visit Russia before Jan 1, 2027?

- Secondary rule before: Physical presence within the geographic boundaries of the area is required. Flying over without landing, layovers during which the person remains in the airplane or airport, virtual or remote appearances, future visit plans, or (unless explicitly specified) presence in adjacent international waters
- Secondary rule after: The following do NOT constitute a visit:  Flying over the area without landing Layovers during which the person remains in an airplane Virtual or remote appearances Presence in international waters adjacent to the area Presence solely within embassy or consulate grounds Plans, announcements, or sche

**KXKASHRUSSIA-26JUL27-NOV01** — Will Kash Patel visit Russia before Nov 1, 2026?

- Secondary rule before: Physical presence within the geographic boundaries is required - flying over without landing, airport layovers where the person remains in the airplane or airport, virtual appearances, presence in international waters, or presence solely within embassy/consulate grounds do NOT count as visits. For c
- Secondary rule after: The following do NOT constitute a visit:  Flying over the area without landing Layovers during which the person remains in an airplane Virtual or remote appearances Presence in international waters adjacent to the area Presence solely within embassy or consulate grounds Plans, announcements, or sche

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26SEP13-T75 | Will there be more than 75 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T45 | Will there be more than 45 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T100 | Will there be more than 100 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |
| KXHORMUZWEEKLY-26SEP13-T10 | Will there be more than 10 transit calls through the Strait of Hormuz from Sep 7, 2026 to Sep 13, 2026? | 2026-09-15 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
