# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-10-18T20:47:12Z
**Since:** 2026-10-11T20:47:12Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 2.71 | 4.14 | +1.43 | 167 h | toward H1, H4 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.08 | 0.33 | +0.26 | 167 h | toward H1, H4; away from H3, H5 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-NOV01 | kalshi:KXKASHRUSSIA-26JUL27-NOV01 | 2026-11-01T15:00:00Z | 23.0% | 8.0% | -15.0 pts | 167 h | away from H6 |
| Polymarket: US-Iran Hormuz agreement — October 31 | polymarket:us-iran-hormuz-agreement-by-october-31 | 2026-11-01T03:59:00Z | 12.8% | 6.8% | -6.0 pts | 167 h | away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure — December 31 | polymarket:russia-x-ukraine-ceasefire-agreement-by-december-31-2026 | 2027-01-01T04:59:00Z | 17.5% | 12.5% | -5.0 pts | 167 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 23.5% | 18.5% | -5.0 pts | 167 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — November 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-november-30-2027 | 2027-12-01T04:59:00Z | 68.0% | 63.0% | -5.0 pts | 167 h | away from H2, H3 |
| Polymarket: NATO-Russia military clash — December 31 | polymarket:nato-x-russia-military-clash-by-december-31-2026-244-538-582 | 2027-01-01T04:59:00Z | 20.5% | 25.5% | +5.0 pts | 167 h | toward H5 |
| Polymarket: Russia-Ukraine ceasefire term structure — November 30 | polymarket:russia-x-ukraine-ceasefire-agreement-by-november-30-2026 | 2026-12-01T04:59:00Z | 10.0% | 6.0% | -4.0 pts | 167 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — August 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-august-31-2027 | 2027-09-01T03:59:00Z | 58.0% | 54.0% | -4.0 pts | 167 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — March 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-march-31-2027 | 2027-04-01T03:59:00Z | 34.0% | 30.5% | -3.5 pts | 167 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — July 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-july-31-2027 | 2027-08-01T03:59:00Z | 54.0% | 50.5% | -3.5 pts | 167 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — September 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-september-30-2027 | 2027-10-01T03:59:00Z | 60.5% | 57.0% | -3.5 pts | 167 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — October 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-october-31-2027 | 2027-11-01T03:59:00Z | 64.5% | 61.0% | -3.5 pts | 167 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — June 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-june-30-2027 | 2027-07-01T03:59:00Z | 51.0% | 48.0% | -3.0 pts | 167 h | away from H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_17 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26OCT18-T22 | Will there be more than 22 transit calls through the Strait of Hormuz from Oct 12, 2026 to Oct 18, 2026? | 2026-10-20 |
| KXHORMUZWEEKLY-26OCT25-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |
| KXHORMUZWEEKLY-26OCT25-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Oct 19, 2026 to Oct 25, 2026? | 2026-10-27 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
