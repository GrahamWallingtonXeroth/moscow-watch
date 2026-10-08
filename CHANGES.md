# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-10-08T06:09:15Z
**Since:** 2026-10-01T06:09:15Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 2 | 1 | -1 | 161 h | toward H3, H5; away from H1, H4 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.14 | 2.71 | -0.43 | 161 h | away from H1, H4 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.5 | 0.15 | -0.35 | 161 h | toward H3, H5; away from H1, H4 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-NOV01 | kalshi:KXKASHRUSSIA-26JUL27-NOV01 | 2026-11-01T15:00:00Z | 4.0% | 21.0% | +17.0 pts | 161 h | toward H6 |
| Polymarket: US-Iran Hormuz agreement — December 31 | polymarket:us-iran-hormuz-agreement-by-december-31 | 2027-01-01T04:59:00Z | 44.5% | 37.0% | -7.5 pts | 161 h | away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure — September 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-september-30-2027 | 2027-10-01T03:59:00Z | 57.0% | 61.5% | +4.5 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 18.5% | 22.5% | +4.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — November 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-november-30-2027 | 2027-12-01T04:59:00Z | 63.0% | 67.0% | +4.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — April 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-april-30-2027 | 2027-05-01T03:59:00Z | 40.5% | 37.5% | -3.0 pts | 161 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — October 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-october-31-2027 | 2027-11-01T03:59:00Z | 60.0% | 63.0% | +3.0 pts | 161 h | toward H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_21 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

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
| [Russian Offensive Campaign Assessment, September 30, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-30-2026) | 2026-09-30 | 2026-10-05T17:24:21Z | sitemap `lastmod` changed |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
