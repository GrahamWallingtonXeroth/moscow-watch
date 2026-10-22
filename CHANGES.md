# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-10-22T04:52:10Z
**Since:** 2026-10-15T04:52:10Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 3 | 1 | -2 | 161 h | toward H3, H5; away from H1, H4 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 4.14 | 3.71 | -0.43 | 161 h | away from H1, H4 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-NOV01 | kalshi:KXKASHRUSSIA-26JUL27-NOV01 | 2026-11-01T15:00:00Z | 23.0% | 4.0% | -19.0 pts | 161 h | away from H6 |
| Kalshi: Zelensky-Putin meeting — KXZELENSKYPUTIN-29-27 | kalshi:KXZELENSKYPUTIN-29-27 | 2027-01-01T04:59:00Z | 6.1% | 15.0% | +8.9 pts | 161 h | toward H2 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.36 | 0.43 | +0.07 | 161 h | toward H1, H4; away from H3, H5 |
| Polymarket: Russia-Ukraine ceasefire term structure — March 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-march-31-2027 | 2027-04-01T03:59:00Z | 31.5% | 37.5% | +6.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — June 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-june-30-2027 | 2027-07-01T03:59:00Z | 49.5% | 55.5% | +6.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — November 30 | polymarket:russia-x-ukraine-ceasefire-agreement-by-november-30-2026 | 2026-12-01T04:59:00Z | 7.5% | 12.5% | +5.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — April 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-april-30-2027 | 2027-05-01T03:59:00Z | 38.5% | 43.5% | +5.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — May 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-may-31-2027 | 2027-06-01T03:59:00Z | 47.0% | 52.0% | +5.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — July 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-july-31-2027 | 2027-08-01T03:59:00Z | 52.5% | 57.5% | +5.0 pts | 161 h | toward H2, H3 |
| Polymarket: US gives Ukraine a formal security guarantee — U.S. agrees to give Ukraine security guarantee by December 31? | polymarket:us-agrees-to-give-ukraine-security-guarantee-by-december-31 | 2027-01-01T04:59:00Z | 4.2% | 8.8% | +4.6 pts | 161 h | toward H5; away from H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 22.5% | 26.5% | +4.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — February 28, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-february-28-2027 | 2027-03-01T04:59:00Z | 28.0% | 32.0% | +4.0 pts | 161 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — December 31 | polymarket:russia-x-ukraine-ceasefire-agreement-by-december-31-2026 | 2027-01-01T04:59:00Z | 17.5% | 20.5% | +3.0 pts | 161 h | toward H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Polymarket: US gives Ukraine a formal security guarantee** — One of the two market inputs to the US-posture axis of the discriminator map. A fall is relief toward Moscow.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_18 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26OCT25-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T27 | Will there be more than 27 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |

## New or modified analytical references

Link metadata only: appearance here does not attest any claim in the linked analysis or count its cited sources twice.

| Assessment | Assessment date | Sitemap modified | Change |
| --- | --- | --- | --- |
| [Russian Offensive Campaign Assessment, October 18, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-18-2026) | 2026-10-18 | 2026-10-18T23:33:11Z | new |
| [Russian Offensive Campaign Assessment, October 17, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-17-2026) | 2026-10-17 | 2026-10-18T00:21:39Z | new |
| [Russian Offensive Campaign Assessment, October 16, 2026](https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-october-16-2026) | 2026-10-16 | 2026-10-17T03:49:10Z | new |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
