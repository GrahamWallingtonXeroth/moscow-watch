# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-11-13T19:45:49Z
**Since:** 2026-11-06T19:45:49Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 7 | 1 | -6 | 158 h | toward H3, H5; away from H1, H4 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.29 | 3.86 | +0.57 | 151 h | toward H1, H4 |
| Polymarket: US-Iran Hormuz agreement — December 31 | polymarket:us-iran-hormuz-agreement-by-december-31 | 2027-01-01T04:59:00Z | 35.5% | 22.5% | -13.0 pts | 158 h | away from H1, H4 |
| Polymarket: US-Iran Hormuz agreement — November 30 | polymarket:us-iran-hormuz-agreement-by-november-30 | 2026-12-01T04:59:00Z | 18.5% | 8.5% | -10.0 pts | 158 h | away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure — August 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-august-31-2027 | 2027-09-01T03:59:00Z | 63.0% | 60.0% | -3.0 pts | 158 h | away from H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.

_25 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXUSAIRANAGREEMENT-27-27OCT | Will the US agree to a new Iranian nuclear deal this year? | 2027-10-01 |
| KXUSAIRANAGREEMENT-27-27JUL | Will the US agree to a new Iranian nuclear deal this year? | 2027-07-01 |
| KXHORMUZWEEKLY-26NOV22-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T27 | Will there be more than 27 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T23 | Will there be more than 23 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
