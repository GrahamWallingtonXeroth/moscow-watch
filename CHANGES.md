# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-09-01T11:43:09Z  
**Since:** 2026-08-25T11:43:09Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator | Then | Now | Move | Window | Points |
| --- | ---: | ---: | ---: | ---: | --- |
| Polymarket: US-Iran ceasefire continues | 83.5% | 0.1% | -83.4 pts | 98 h | away from H1, H4 |
| Kalshi: Witkoff travels to Russia | 59.0% | 39.0% | -20.0 pts | 136 h | away from H2 |
| Russia-Iran engagement volume (reporting index) | 0.26 | 0.44 | +0.17 | 122 h | toward H1, H4; away from H3, H5 |
| Polymarket: US-Iran Hormuz agreement | 16.5% | 8.0% | -8.5 pts | 136 h | away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure | 0.8% | 9.0% | +8.2 pts | 136 h | toward H2, H3 |
| Kalshi: Putin-Trump meeting location | 11.0% | 5.0% | -6.0 pts | 136 h | away from H2 |
| Polymarket: NATO-Russia military clash | 29.5% | 24.0% | -5.5 pts | 136 h | away from H5 |

- **Kalshi: Witkoff travels to Russia** — A named envoy trip is one of the cleaner observable proxies for an active Ukraine track.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs are thin - under $5,000 of volume - so treat the Q1-2027 peak with the caution that deserves.

_6 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

## Resolution wording and new markets

A change to resolution wording is a material event: the same ticker can silently start meaning something different, and a chart plotted straight through such a change is misleading.

### Resolution wording changed

**KXWITKOFFRUSSIA-26JUN29-OCT01** — Will Steve Witkoff visit Russia before Oct 1, 2026?

- Before: If Steve Witkoff has physically travelled to and been present within the geographic boundaries of Russia before Oct 1, 2026, then the market resolves to Yes.
- After: If Steve Witkoff has physically travelled to and been present within the geographic boundaries of Russia before Oct 1, 2026, then the market resolves to Yes.

**KXWITKOFFRUSSIA-26JUN29-JAN01** — Will Steve Witkoff visit Russia before Jan 1, 2027?

- Before: If Steve Witkoff has physically travelled to and been present within the geographic boundaries of Russia before Jan 1, 2027, then the market resolves to Yes.
- After: If Steve Witkoff has physically travelled to and been present within the geographic boundaries of Russia before Jan 1, 2027, then the market resolves to Yes.

**KXKASHRUSSIA-26JUL27-NOV01** — Will Kash Patel visit Russia before Nov 1, 2026?

- Before: If Kash Patel has physically travelled to and been present within the geographic boundaries of Russia before Nov 1, 2026, then the market resolves to Yes.
- After: If Kash Patel has physically travelled to and been present within the geographic boundaries of Russia before Nov 1, 2026, then the market resolves to Yes.

### New markets listed in a tracked series

| Ticker | Title | Closes |
| --- | --- | --- |
| KXHORMUZWEEKLY-26SEP06-T75 | Will there be more than 75 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T50 | Will there be more than 50 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T45 | Will there be more than 45 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T40 | Will there be more than 40 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T35 | Will there be more than 35 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T30 | Will there be more than 30 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T25 | Will there be more than 25 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T20 | Will there be more than 20 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T15 | Will there be more than 15 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T100 | Will there be more than 100 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |
| KXHORMUZWEEKLY-26SEP06-T10 | Will there be more than 10 transit calls through the Strait of Hormuz from Aug 31, 2026 to Sep 6, 2026? | 2026-09-08 |

---

Rendered by `mw diff`. The tracker itself is [TRACKER.md](TRACKER.md).
