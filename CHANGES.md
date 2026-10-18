# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-10-18T11:11:01Z
**Since:** 2026-10-11T11:11:01Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 2.71 | 4.14 | +1.43 | 166 h | toward H1, H4 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.08 | 0.33 | +0.26 | 166 h | toward H1, H4; away from H3, H5 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-NOV01 | kalshi:KXKASHRUSSIA-26JUL27-NOV01 | 2026-11-01T15:00:00Z | 23.0% | 8.0% | -15.0 pts | 166 h | away from H6 |
| Polymarket: Russia-Ukraine ceasefire term structure — November 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-november-30-2027 | 2027-12-01T04:59:00Z | 67.0% | 62.5% | -4.5 pts | 166 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 21.5% | 18.5% | -3.0 pts | 166 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — September 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-september-30-2027 | 2027-10-01T03:59:00Z | 60.0% | 57.0% | -3.0 pts | 166 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — October 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-october-31-2027 | 2027-11-01T03:59:00Z | 63.5% | 60.5% | -3.0 pts | 166 h | away from H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_23 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

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
