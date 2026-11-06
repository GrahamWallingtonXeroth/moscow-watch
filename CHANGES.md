# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-11-06T06:52:35Z
**Since:** 2026-10-30T06:52:35Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 4 | 7 | +3 | 162 h | toward H1, H4; away from H3, H5 |
| Polymarket: US gives Ukraine a formal security guarantee — June 30, 2027 | polymarket:us-agrees-to-give-ukraine-security-guarantee-by-june-30-2027 | 2027-07-01T03:59:00Z | 53.5% | 22.0% | -31.5 pts | 162 h | toward H3; away from H5 |
| Polymarket: US gives Ukraine a formal security guarantee — December 31, 2027 | polymarket:us-agrees-to-give-ukraine-security-guarantee-by-december-31-2027 | 2028-01-01T04:59:00Z | 54.5% | 26.5% | -28.0 pts | 162 h | toward H3; away from H5 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-JAN01 | kalshi:KXKASHRUSSIA-26JUL27-JAN01 | 2027-01-01T15:00:00Z | 24.0% | 1.0% | -23.0 pts | 162 h | away from H6 |
| Russia-Iran engagement volume (reporting index) | — | — | 0.3 | 0.42 | +0.12 | 162 h | toward H1, H4; away from H3, H5 |
| Polymarket: final US-Iran nuclear deal — November 30 | polymarket:us-iran-final-nuclear-deal-by-november-30-2026 | 2026-12-01T04:59:00Z | 8.0% | 2.9% | -5.1 pts | 162 h | away from H1, H4 |
| Polymarket: NATO-Russia military clash — December 31 | polymarket:nato-x-russia-military-clash-by-december-31-2026-244-538-582 | 2027-01-01T04:59:00Z | 16.5% | 11.5% | -5.0 pts | 162 h | away from H5 |
| Kalshi: US-Iran nuclear agreement — KXUSAIRANAGREEMENT-27-26DEC | kalshi:KXUSAIRANAGREEMENT-27-26DEC | 2026-12-01T15:00:00Z | 7.0% | 2.0% | -5.0 pts | 162 h | away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure — March 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-march-31-2027 | 2027-04-01T03:59:00Z | 33.5% | 38.0% | +4.5 pts | 162 h | toward H2, H3 |

- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Polymarket: US gives Ukraine a formal security guarantee** — One of the two market inputs to the US-posture axis of the discriminator map. A fall is relief toward Moscow.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.

_22 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26NOV08-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T27 | Will there be more than 27 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T23 | Will there be more than 23 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |
| KXHORMUZWEEKLY-26NOV08-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Nov 2, 2026 to Nov 8, 2026? | 2026-11-10 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
