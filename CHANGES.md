# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-11-20T20:25:12Z
**Since:** 2026-11-13T20:25:12Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 2 | 7 | +5 | 158 h | toward H1, H4; away from H3, H5 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.86 | 2.29 | -1.57 | 158 h | away from H1, H4 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.33 | 0.64 | +0.31 | 158 h | toward H1, H4; away from H3, H5 |
| Polymarket: US-Iran Hormuz agreement — December 31 | polymarket:us-iran-hormuz-agreement-by-december-31 | 2027-01-01T04:59:00Z | 21.5% | 10.0% | -11.5 pts | 158 h | away from H1, H4 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-JAN01 | kalshi:KXKASHRUSSIA-26JUL27-JAN01 | 2027-01-01T15:00:00Z | 1.0% | 8.0% | +7.0 pts | 158 h | toward H6 |
| Polymarket: Russia-Ukraine ceasefire term structure — March 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-march-31-2027 | 2027-04-01T03:59:00Z | 35.5% | 29.0% | -6.5 pts | 158 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — February 28, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-february-28-2027 | 2027-03-01T04:59:00Z | 27.5% | 22.5% | -5.0 pts | 158 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — January 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-january-31-2027 | 2027-02-01T04:59:00Z | 22.5% | 18.5% | -4.0 pts | 158 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — May 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-may-31-2027 | 2027-06-01T03:59:00Z | 51.0% | 54.5% | +3.5 pts | 158 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — June 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-june-30-2027 | 2027-07-01T03:59:00Z | 53.0% | 56.5% | +3.5 pts | 158 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — July 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-july-31-2027 | 2027-08-01T03:59:00Z | 57.5% | 60.5% | +3.0 pts | 158 h | toward H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_18 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26NOV15-T24 | Will there be more than 24 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T22 | Will there be more than 22 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T21 | Will there be more than 21 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV22-T12 | Will there be more than 12 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T10 | Will there be more than 10 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T5 | Will there be more than 5 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXPUTINDJTLOCATION-29B-VNM | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-USA | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-UAE | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-TUR | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-SWZ | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-SARA | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-RUS | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-QAT | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-PRC | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-MEX | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-KOR | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-HUN | Where will Trump and Putin next meet? | 2029-01-01 |
| KXPUTINDJTLOCATION-29B-AUT | Where will Trump and Putin next meet? | 2029-01-01 |
| KXHORMUZWEEKLY-26NOV22-T14 | Will there be more than 14 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |
| KXHORMUZWEEKLY-26NOV22-T13 | Will there be more than 13 transit calls through the Strait of Hormuz from Nov 16, 2026 to Nov 22, 2026? | 2026-11-24 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
