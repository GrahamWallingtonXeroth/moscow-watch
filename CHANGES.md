# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-09-22T05:01:10Z
**Since:** 2026-09-15T05:01:10Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 4 | 1 | -3 | 161 h | toward H3, H5; away from H1, H4 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.14 | 5.29 | +2.14 | 161 h | toward H1, H4 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-NOV01 | kalshi:KXKASHRUSSIA-26JUL27-NOV01 | 2026-11-01T15:00:00Z | 28.0% | 12.0% | -16.0 pts | 161 h | away from H6 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 34.5% | 27.5% | -7.0 pts | 161 h | away from H2, H3 |
| Polymarket: NATO-Russia military clash — October 31 | polymarket:nato-x-russia-military-clash-by-october-31-2026 | 2026-11-01T03:59:00Z | 14.5% | 21.5% | +7.0 pts | 161 h | toward H5 |
| Polymarket: NATO-Russia military clash — December 31 | polymarket:nato-x-russia-military-clash-by-december-31-2026-244-538-582 | 2027-01-01T04:59:00Z | 26.0% | 32.5% | +6.5 pts | 161 h | toward H5 |
| Kalshi: Zelensky-Putin meeting — KXZELENSKYPUTIN-29-27 | kalshi:KXZELENSKYPUTIN-29-27 | 2027-01-01T04:59:00Z | 16.0% | 9.9% | -6.1 pts | 161 h | away from H2 |
| Polymarket: Russia-Ukraine ceasefire term structure — December 31 | polymarket:russia-x-ukraine-ceasefire-agreement-by-december-31-2026 | 2027-01-01T04:59:00Z | 25.0% | 20.5% | -4.5 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — February 28, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-february-28-2027 | 2027-03-01T04:59:00Z | 36.5% | 32.0% | -4.5 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — June 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-june-30-2027 | 2027-07-01T03:59:00Z | 57.5% | 54.0% | -3.5 pts | 161 h | away from H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.

_21 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26SEP27-T75 | Will there be more than 75 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T45 | Will there be more than 45 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T100 | Will there be more than 100 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |
| KXHORMUZWEEKLY-26SEP27-T10 | Will there be more than 10 transit calls through the Strait of Hormuz from Sep 21, 2026 to Sep 27, 2026? | 2026-09-29 |

## New or modified analytical references

Link metadata only: appearance here does not attest any claim in the linked analysis or count its cited sources twice.

| Assessment | Assessment date | Sitemap modified | Change |
| --- | --- | --- | --- |
| [Russian Offensive Campaign Assessment, September 21, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-21-2026) | 2026-09-21 | 2026-09-22T00:34:58Z | new |
| [Russian Offensive Campaign Assessment, September 20, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-20-2026) | 2026-09-20 | 2026-09-21T18:59:57Z | new |
| [Russian Offensive Campaign Assessment, September 19, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-19-2026) | 2026-09-19 | 2026-09-21T18:57:43Z | new |
| [Russian Offensive Campaign Assessment, September 18, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-18-2026) | 2026-09-18 | 2026-09-19T03:03:42Z | new |
| [Russian Offensive Campaign Assessment, September 17, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-17-2026) | 2026-09-17 | 2026-09-18T03:39:18Z | new |
| [Russian Offensive Campaign Assessment, September 16, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-16-2026) | 2026-09-16 | 2026-09-17T13:34:33Z | new |
| [Russian Offensive Campaign Assessment, September 15, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-15-2026) | 2026-09-15 | 2026-09-16T02:57:08Z | new |
| [Russian Offensive Campaign Assessment, September 14, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-14-2026) | 2026-09-14 | 2026-09-16T02:08:28Z | sitemap `lastmod` changed |
| [Russian Offensive Campaign Assessment, September 12, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-12-2026) | 2026-09-12 | 2026-09-16T02:09:40Z | sitemap `lastmod` changed |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
