# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-10-31T05:46:45Z
**Since:** 2026-10-24T05:46:45Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 1 | 5 | +4 | 163 h | toward H1, H4; away from H3, H5 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.71 | 3.29 | -0.43 | 146 h | away from H1, H4 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.45 | 0.3 | -0.15 | 163 h | toward H3, H5; away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure — December 31 | polymarket:russia-x-ukraine-ceasefire-agreement-by-december-31-2026 | 2027-01-01T04:59:00Z | 21.5% | 14.5% | -7.0 pts | 163 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — November 30 | polymarket:russia-x-ukraine-ceasefire-agreement-by-november-30-2026 | 2026-12-01T04:59:00Z | 12.0% | 6.5% | -5.5 pts | 163 h | away from H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_30 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26NOV08-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T27 | Will there be more than 27 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T23 | Will there be more than 23 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
