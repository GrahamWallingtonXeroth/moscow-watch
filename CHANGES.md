# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-10-09T22:41:42Z
**Since:** 2026-10-02T22:41:42Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 1 | 3 | +2 | 161 h | toward H1, H4; away from H3, H5 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.14 | 2.71 | -0.43 | 161 h | away from H1, H4 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.43 | 0.15 | -0.28 | 161 h | toward H3, H5; away from H1, H4 |
| Polymarket: US-Iran Hormuz agreement — December 31 | polymarket:us-iran-hormuz-agreement-by-december-31 | 2027-01-01T04:59:00Z | 41.5% | 35.5% | -6.0 pts | 161 h | away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure — October 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-october-31-2027 | 2027-11-01T03:59:00Z | 60.5% | 63.5% | +3.0 pts | 161 h | toward H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_26 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXZELENSKYPUTIN-29-28 | Volodymyr Zelenskyy and Vladimir Putin meet before Jan 1, 2028? | 2028-01-01 |
| KXKASHRUSSIA-26JUL27-JAN01 | Will Kash Patel visit Russia before Jan 1, 2027? | 2027-01-01 |
| KXHORMUZWEEKLY-26OCT11-T22 | Will there be more than 22 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZNORM-26MAR17-B271201 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before December 1, 2027? | 2027-12-07 |
| KXHORMUZNORM-26MAR17-B271101 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before November 1, 2027? | 2027-11-02 |
| KXHORMUZNORM-26MAR17-B271001 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before October 1, 2027? | 2027-10-05 |
| KXHORMUZNORM-26MAR17-B270901 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before September 1, 2027? | 2027-09-07 |
| KXHORMUZNORM-26MAR17-B270801 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before August 1, 2027? | 2027-08-03 |
| KXHORMUZNORM-26MAR17-B270601 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before June 1, 2027? | 2027-06-08 |
| KXHORMUZNORM-26MAR17-B270501 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before May 1, 2027? | 2027-05-04 |
| KXHORMUZNORM-26MAR17-B270301 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before March 1, 2027? | 2027-03-02 |
| KXHORMUZNORM-26MAR17-B270201 | Will the 7-day moving average of transit calls through the Strait of Hormuz as reported by the IMF PortWatch be above 60 before February 1, 2027? | 2027-02-02 |
| KXHORMUZWEEKLY-26OCT18-T75 | Will there be more than 75 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T45 | Will there be more than 45 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T100 | Will there be more than 100 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT18-T10 | Will there be more than 10 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |

## New or modified analytical references

Link metadata only: appearance here does not attest any claim in the linked analysis or count its cited sources twice.

| Assessment | Assessment date | Sitemap modified | Change |
| --- | --- | --- | --- |
| [Russian Offensive Campaign Assessment, October 8, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-8-2026) | 2026-10-08 | 2026-10-09T03:35:12Z | new |
| [Russian Offensive Campaign Assessment, October 7, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-7-2026) | 2026-10-07 | 2026-10-07T23:17:24Z | new |
| [Russian Offensive Campaign Assessment, October 6, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-6-2026) | 2026-10-06 | 2026-10-07T01:38:04Z | new |
| [Russian Offensive Campaign Assessment, October 5, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-5-2026) | 2026-10-05 | 2026-10-05T22:29:06Z | new |
| [Russian Offensive Campaign Assessment, October 4, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-4-2026) | 2026-10-04 | 2026-10-05T18:48:59Z | new |
| [Russian Offensive Campaign Assessment, October 3, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-3-2026) | 2026-10-03 | 2026-10-05T17:59:10Z | new |
| [Russian Offensive Campaign Assessment, October 2, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-2-2026) | 2026-10-02 | 2026-10-05T16:40:09Z | new |
| [Russian Offensive Campaign Assessment, October 1, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-1-2026) | 2026-10-01 | 2026-10-05T19:33:14Z | sitemap `lastmod` changed |
| [Russian Offensive Campaign Assessment, September 30, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-30-2026) | 2026-09-30 | 2026-10-05T17:24:21Z | sitemap `lastmod` changed |
| [Russian Offensive Campaign Assessment, September 14, 2024](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-14-2024) | 2024-09-14 | 2026-10-06T20:45:25Z | new |
| [Russian Offensive Campaign Assessment, May 25, 2024](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-may-25-2024) | 2024-05-25 | 2026-10-06T20:47:12Z | new |
| [Russian Offensive Campaign Assessment, May 21, 2024](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-may-21-2024) | 2024-05-21 | 2026-10-06T20:47:18Z | new |
| [Russian Offensive Campaign Assessment, December 14, 2023](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-december-14-2023) | 2023-12-14 | 2026-10-06T20:50:35Z | new |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
