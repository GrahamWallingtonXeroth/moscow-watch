# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-11-09T06:36:40Z
**Since:** 2026-11-02T06:36:40Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator / leg | Exact contract ID | Deadline (UTC) | Then | Now | Move | Window | Points |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Reported senior Russia-Iran diplomatic contacts per fortnight | — | — | 5 | 7 | +2 | 159 h | toward H1, H4; away from H3, H5 |
| IMF PortWatch: daily Strait of Hormuz transits | — | — | 3.29 | 4.43 | +1.14 | 159 h | toward H1, H4 |
| Kalshi: Kash Patel travels to Russia — KXKASHRUSSIA-26JUL27-JAN01 | kalshi:KXKASHRUSSIA-26JUL27-JAN01 | 2027-01-01T15:00:00Z | 14.0% | 1.0% | -13.0 pts | 159 h | away from H6 |
| Polymarket: US-Iran Hormuz agreement — November 30 | polymarket:us-iran-hormuz-agreement-by-november-30 | 2026-12-01T04:59:00Z | 27.5% | 15.5% | -12.0 pts | 159 h | away from H1, H4 |
| Polymarket: final US-Iran nuclear deal — November 30 | polymarket:us-iran-final-nuclear-deal-by-november-30-2026 | 2026-12-01T04:59:00Z | 8.5% | 2.4% | -6.2 pts | 159 h | away from H1, H4 |
| Polymarket: US gives Ukraine a formal security guarantee — December 31, 2027 | polymarket:us-agrees-to-give-ukraine-security-guarantee-by-december-31-2027 | 2028-01-01T04:59:00Z | 32.0% | 26.0% | -6.0 pts | 159 h | toward H3; away from H5 |
| Kalshi: US-Iran nuclear agreement — KXUSAIRANAGREEMENT-27-26DEC | kalshi:KXUSAIRANAGREEMENT-27-26DEC | 2026-12-01T15:00:00Z | 7.0% | 2.0% | -5.0 pts | 159 h | away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure — December 31 | polymarket:russia-x-ukraine-ceasefire-agreement-by-december-31-2026 | 2027-01-01T04:59:00Z | 12.5% | 15.5% | +3.0 pts | 159 h | toward H2, H3 |
| Polymarket: Russia-Ukraine ceasefire term structure — July 31, 2027 | polymarket:russia-x-ukraine-ceasefire-agreement-by-july-31-2027 | 2027-08-01T03:59:00Z | 57.0% | 60.0% | +3.0 pts | 159 h | toward H2, H3 |

- **IMF PortWatch: daily Strait of Hormuz transits** — The project's one counted physical quantity. Updates weekly with roughly a week to ten days of lag, so the newest row is never today, and the lag is printed beside every reading. Counts are currently extraordinarily low, consistent with AIS jamming and dark-vessel behaviour in the strait; this measures observed transits, not all transits.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs have materially less turnover than the near-dated legs; inspect the current per-leg volume printed above before interpreting the shape.
- **Polymarket: US gives Ukraine a formal security guarantee** — One of the two market inputs to the US-posture axis of the discriminator map. A fall is relief toward Moscow.
- **Reported senior Russia-Iran diplomatic contacts per fortnight** — The directly counted half of what separates H3 from H4. Both predict the same Iran outcomes; what tells them apart is which direction Russian officials are travelling. Counts REPORTED contacts only - unreported diplomacy is exactly what this story is about - so it is a floor, never a total. Every counted contact stores its source URL.

_24 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26NOV15-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T27 | Will there be more than 27 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T23 | Will there be more than 23 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXHORMUZWEEKLY-26NOV15-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Nov 9, 2026 to Nov 15, 2026? | 2026-11-17 |
| KXUSAIRANAGREEMENT-27-27OCT | Will the US agree to a new Iranian nuclear deal this year? | 2027-10-01 |
| KXUSAIRANAGREEMENT-27-27JUL | Will the US agree to a new Iranian nuclear deal this year? | 2027-07-01 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
