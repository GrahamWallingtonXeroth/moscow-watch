# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-11-12T19:57:58Z
**Since:** 2026-11-05T19:57:58Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 6 | 1 | -5 | 168 h | toward H3, H5; away from H1, H4 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.29 | 3.86 | +0.57 | 168 h | toward H1, H4 |
| Polymarket: US-Iran Hormuz agreement — December 31 | polymarket:us-iran-hormuz-agreement-by-december-31 | 2027-01-01T04:59:00Z | 38.0% | 24.5% | -13.5 pts | 168 h | away from H1, H4 |
| Polymarket: US-Iran Hormuz agreement — November 30 | polymarket:us-iran-hormuz-agreement-by-november-30 | 2026-12-01T04:59:00Z | 19.5% | 8.5% | -11.0 pts | 168 h | away from H1, H4 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.42 | 0.32 | -0.11 | 168 h | toward H3, H5; away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure — December 31 | polymarket:russia-x-ukraine-ceasefire-agreement-by-december-31-2026 | 2027-01-01T04:59:00Z | 15.5% | 12.5% | -3.0 pts | 168 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 21.5% | 24.5% | +3.0 pts | 168 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — October 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-october-31-2027 | 2027-11-01T03:59:00Z | 64.0% | 67.0% | +3.0 pts | 168 h | toward H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_23 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26NOV15-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T27 | Will there be more than 27 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T23 | Will there be more than 23 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXUSAIRANAGREEMENT-27-27OCT | Will the US agree to a new Iranian nuclear deal this year? | 2027-10-01 |
| KXUSAIRANAGREEMENT-27-27JUL | Will the US agree to a new Iranian nuclear deal this year? | 2027-07-01 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
