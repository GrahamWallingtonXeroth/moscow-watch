# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-10-06T06:25:12Z
**Since:** 2026-09-29T06:25:11Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 2 | 1 | -1 | 161 h | toward H3, H5; away from H1, H4 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-NOV01 | kalshi:KXKASHRUSSIA-26JUL27-NOV01 | 2026-11-01T15:00:00Z | 4.0% | 50.0% | +46.0 pts | 161 h | toward H6 |
| Polymarket: US-Iran Hormuz agreement — November 30 | polymarket:us-iran-hormuz-agreement-by-november-30 | 2026-12-01T04:59:00Z | 49.0% | 22.5% | -26.5 pts | 161 h | away from H1, H4 |
| Polymarket: US-Iran Hormuz agreement — October 31 | polymarket:us-iran-hormuz-agreement-by-october-31 | 2026-11-01T03:59:00Z | 37.0% | 13.5% | -23.5 pts | 161 h | away from H1, H4 |
| Polymarket: US-Iran Hormuz agreement — December 31 | polymarket:us-iran-hormuz-agreement-by-december-31 | 2027-01-01T04:59:00Z | 55.0% | 33.0% | -22.0 pts | 161 h | away from H1, H4 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.54 | 0.43 | -0.11 | 161 h | toward H3, H5; away from H1, H4 |
| Polymarket: US-Iran Hormuz agreement — October 15 | polymarket:us-iran-hormuz-agreement-by-october-15 | 2026-10-16T03:59:00Z | 16.0% | 6.5% | -9.5 pts | 161 h | away from H1, H4 |
| Polymarket: NATO-Russia military clash — December 31 | polymarket:nato-x-russia-military-clash-by-december-31-2026-244-538-582 | 2027-01-01T04:59:00Z | 28.5% | 21.5% | -7.0 pts | 161 h | away from H5 |
| Polymarket: Russia-Ukraine ceasefire term structure — April 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-april-30-2027 | 2027-05-01T03:59:00Z | 43.0% | 38.0% | -5.0 pts | 161 h | away from H2, H3 |
| Polymarket: NATO-Russia military clash — October 31 | polymarket:nato-x-russia-military-clash-by-october-31-2026 | 2026-11-01T03:59:00Z | 13.5% | 8.5% | -5.0 pts | 161 h | away from H5 |
| Polymarket: Russia-Ukraine ceasefire term structure — February 28, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-february-28-2027 | 2027-03-01T04:59:00Z | 29.5% | 25.0% | -4.5 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 26.5% | 22.5% | -4.0 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — March 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-march-31-2027 | 2027-04-01T03:59:00Z | 37.5% | 33.5% | -4.0 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — June 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-june-30-2027 | 2027-07-01T03:59:00Z | 53.5% | 49.5% | -4.0 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — December 31 | polymarket:russia-x-ukraine-ceasefire-agreement-by-december-31-2026 | 2027-01-01T04:59:00Z | 18.5% | 15.0% | -3.5 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — May 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-may-31-2027 | 2027-06-01T03:59:00Z | 49.5% | 46.0% | -3.5 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — November 30 | polymarket:russia-x-ukraine-ceasefire-agreement-by-november-30-2026 | 2026-12-01T04:59:00Z | 11.5% | 8.5% | -3.0 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — July 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-july-31-2027 | 2027-08-01T03:59:00Z | 56.0% | 53.0% | -3.0 pts | 161 h | away from H2, H3 |

- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_13 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26OCT11-T75 | Will there be more than 75 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T45 | Will there be more than 45 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T100 | Will there be more than 100 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |
| KXHORMUZWEEKLY-26OCT11-T10 | Will there be more than 10 transit calls through the Strait of Hormuz from Oct 5, 2026 to Oct 11, 2026? | 2026-10-13 |

## New or modified analytical references

Link metadata only: appearance here does not attest any claim in the linked analysis or count its cited sources twice.

| Assessment | Assessment date | Sitemap modified | Change |
| --- | --- | --- | --- |
| [Russian Offensive Campaign Assessment, October 5, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-5-2026) | 2026-10-05 | 2026-10-05T22:29:06Z | new |
| [Russian Offensive Campaign Assessment, October 4, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-4-2026) | 2026-10-04 | 2026-10-05T18:48:59Z | new |
| [Russian Offensive Campaign Assessment, October 3, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-3-2026) | 2026-10-03 | 2026-10-05T17:59:10Z | new |
| [Russian Offensive Campaign Assessment, October 2, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-2-2026) | 2026-10-02 | 2026-10-05T16:40:09Z | new |
| [Russian Offensive Campaign Assessment, October 1, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-1-2026) | 2026-10-01 | 2026-10-05T19:33:14Z | new |
| [Russian Offensive Campaign Assessment, September 30, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-30-2026) | 2026-09-30 | 2026-10-05T17:24:21Z | new |
| [Russian Offensive Campaign Assessment, September 29, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-29-2026) | 2026-09-29 | 2026-09-30T13:38:02Z | new |
| [Russian Offensive Campaign Assessment, September 28, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-28-2026) | 2026-09-28 | 2026-09-29T01:13:15Z | new |
| [Russian Offensive Campaign Assessment, September 25, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-25-2026) | 2026-09-25 | 2026-09-29T19:54:38Z | sitemap `lastmod` changed |
| [Russian Offensive Campaign Assessment, September 12, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-12-2026) | 2026-09-12 | 2026-09-29T14:02:32Z | sitemap `lastmod` changed |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
