# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-09-18T20:57:11Z
**Since:** 2026-09-11T20:57:11Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.14 | 5.29 | +2.14 | 168 h | toward H1, H4 |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 2 | 4 | +2 | 168 h | toward H1, H4; away from H3, H5 |
| Kalshi: new US sanctions on Russia — KXSANCTIONRUSSIA-26JUL-NOV | kalshi:KXSANCTIONRUSSIA-26JUL-NOV | 2026-11-01T15:00:00Z | 34.0% | 99.0% | +65.0 pts | 168 h | toward H5; away from H3 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-NOV01 | kalshi:KXKASHRUSSIA-26JUL27-NOV01 | 2026-11-01T15:00:00Z | 32.0% | 14.0% | -18.0 pts | 168 h | away from H6 |
| Polymarket: NATO-Russia military clash — October 31 | polymarket:nato-x-russia-military-clash-by-october-31-2026 | 2026-11-01T03:59:00Z | 7.5% | 15.0% | +7.5 pts | 168 h | toward H5 |
| Kalshi: Putin-Trump meeting location — KXPUTINDJTLOCATION-29-HUN | kalshi:KXPUTINDJTLOCATION-29-HUN | 2029-01-01T04:59:00Z | 10.0% | 4.0% | -6.0 pts | 168 h | away from H2 |
| Polymarket: NATO-Russia military clash — December 31 | polymarket:nato-x-russia-military-clash-by-december-31-2026-244-538-582 | 2027-01-01T04:59:00Z | 23.0% | 28.5% | +5.5 pts | 168 h | toward H5 |
| Kalshi: Zelensky-Putin meeting — KXZELENSKYPUTIN-29-27 | kalshi:KXZELENSKYPUTIN-29-27 | 2027-01-01T04:59:00Z | 9.9% | 15.0% | +5.1 pts | 168 h | toward H2 |
| Polymarket: Russia-Ukraine ceasefire term structure — November 30 | polymarket:russia-x-ukraine-ceasefire-agreement-by-november-30-2026 | 2026-12-01T04:59:00Z | 15.5% | 10.5% | -5.0 pts | 168 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — October 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-october-31-2027 | 2027-11-01T03:59:00Z | 65.5% | 60.5% | -5.0 pts | 168 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 34.0% | 29.5% | -4.5 pts | 168 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — August 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-august-31-2027 | 2027-09-01T03:59:00Z | 63.5% | 59.5% | -4.0 pts | 168 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — February 28, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-february-28-2027 | 2027-03-01T04:59:00Z | 38.5% | 35.5% | -3.0 pts | 168 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — September 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-september-30-2027 | 2027-10-01T03:59:00Z | 64.0% | 61.0% | -3.0 pts | 168 h | away from H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Kalshi: new US sanctions on Russia** — A US-posture input. Costs point to H5 and against the American leg of H3.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.

_18 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHOUSERUSSIASANCTION-26SEP14-T220 | Will a Russia sanctions bill receive above 220 Yea votes in the House? | 2027-01-01 |
| KXHOUSERUSSIASANCTION-26SEP14-T230 | Will a Russia sanctions bill receive above 230 Yea votes in the House? | 2027-01-01 |
| KXHOUSERUSSIASANCTION-26SEP14-T240 | Will a Russia sanctions bill receive above 240 Yea votes in the House? | 2027-01-01 |
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
| [Russian Offensive Campaign Assessment, September 17, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-17-2026) | 2026-09-17 | 2026-09-18T03:39:18Z | new |
| [Russian Offensive Campaign Assessment, September 16, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-16-2026) | 2026-09-16 | 2026-09-17T13:34:33Z | new |
| [Russian Offensive Campaign Assessment, September 15, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-15-2026) | 2026-09-15 | 2026-09-16T02:57:08Z | new |
| [Russian Offensive Campaign Assessment, September 14, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-14-2026) | 2026-09-14 | 2026-09-16T02:08:28Z | new |
| [Russian Offensive Campaign Assessment, September 13, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-13-2026) | 2026-09-13 | 2026-09-14T01:53:30Z | new |
| [Russian Offensive Campaign Assessment, September 12, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-12-2026) | 2026-09-12 | 2026-09-16T02:09:40Z | new |
| [Russian Offensive Campaign Assessment, September 11, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-11-2026) | 2026-09-11 | 2026-09-14T17:01:27Z | new |
| [Russian Offensive Campaign Assessment, September 10, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-10-2026) | 2026-09-10 | 2026-09-11T17:17:48Z | sitemap `lastmod` changed |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
