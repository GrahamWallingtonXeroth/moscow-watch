# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-11-23T23:57:12Z
**Since:** 2026-11-16T23:57:12Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 3 | 8 | +5 | 160 h | toward H1, H4; away from H3, H5 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.35 | 0.5 | +0.15 | 160 h | toward H1, H4; away from H3, H5 |
| Polymarket: Russia-Ukraine ceasefire term structure — March 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-march-31-2027 | 2027-04-01T03:59:00Z | 35.5% | 27.5% | -8.0 pts | 160 h | away from H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — April 30, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-april-30-2027 | 2027-05-01T03:59:00Z | 42.5% | 37.5% | -5.0 pts | 160 h | away from H2, H3 |

- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_21 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
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
| KXHORMUZWEEKLY-26NOV29-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T5 | Will there be more than 5 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T27 | Will there be more than 27 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T23 | Will there be more than 23 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T14 | Will there be more than 14 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T13 | Will there be more than 13 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T12 | Will there be more than 12 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |
| KXHORMUZWEEKLY-26NOV29-T10 | Will there be more than 10 transit calls through the Strait of Hormuz from Nov 23, 2026 to Nov 29, 2026? | 2026-12-01 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
