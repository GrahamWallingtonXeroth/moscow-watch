# Changes

_Generated. Do not edit by hand._

**Generated:** 2026-09-01T16:43:06Z  
**Since:** 2026-08-25T16:43:06Z

Everything below cleared two thresholds fixed in advance: a minimum observation window of 6 hours, and the indicator's own `material_move`. Smaller or faster wobbles are not reported, because they are noise and reporting them as news is how a tracker loses its reader.

A move is not evidence for a hypothesis. It is a change in a number that would *bear on* one, in a direction stated before the move happened.

## Indicators that moved

| Indicator | Then | Now | Move | Window | Points |
| --- | ---: | ---: | ---: | ---: | --- |
| Polymarket: US-Iran ceasefire continues | 83.5% | 0.1% | -83.4 pts | 98 h | away from H1, H4 |
| Kalshi: Kash Patel travels to Russia | 65.0% | 40.0% | -25.0 pts | 141 h | away from H6 |
| Kalshi: Witkoff travels to Russia | 59.0% | 39.0% | -20.0 pts | 141 h | away from H2 |
| Russia-Iran engagement volume (reporting index) | 0.26 | 0.44 | +0.17 | 127 h | toward H1, H4; away from H3, H5 |
| Kalshi: new US sanctions on Russia | 5.0% | 15.0% | +10.0 pts | 141 h | toward H5; away from H3 |
| Kalshi: weekly Strait of Hormuz traffic | 10.0% | 0.0% | -10.0 pts | 141 h | away from H1, H4 |
| Polymarket: US-Iran Hormuz agreement | 16.5% | 8.5% | -8.0 pts | 141 h | away from H1, H4 |
| Polymarket: Russia-Ukraine ceasefire term structure | 0.8% | 7.5% | +6.8 pts | 141 h | toward H2, H3 |
| Kalshi: Putin-Trump meeting location | 11.0% | 5.0% | -6.0 pts | 141 h | away from H2 |

- **Kalshi: Witkoff travels to Russia** — A named envoy trip is one of the cleaner observable proxies for an active Ukraine track.
- **Russia-Iran engagement volume (reporting index)** — Counts REPORTING VOLUME from a news index - GDELT DOC 2.0 in timelinevol mode - and not contacts. It is a proxy for diplomatic tempo rather than a count of contacts: the value is the share of monitored world coverage matching the query, averaged over the fortnight. Only the DIRECTION of change against the pre-25-August baseline is meaningful; the level carries no meaning on its own. A GDELT hit still cannot attest a claim, because counting volume and attesting a claim are different operations, so nothing here promotes anything. The directly collected contact counter runs alongside it and is the auditable one.
- **Kalshi: new US sanctions on Russia** — A US-posture input. Costs point to H5 and against the American leg of H3.
- **Kalshi: weekly Strait of Hormuz traffic** — Settles on IMF PortWatch, the same feed this repo collects directly, so the market and the counted quantity can be read against each other.
- **Polymarket: Russia-Ukraine ceasefire term structure** — Read as a ladder, not a price. A parallel shift is sentiment; a change in the shape of the forward hazard curve is news about timing. The far legs are thin - under $5,000 of volume - so treat the Q1-2027 peak with the caution that deserves.

_7 smaller move(s) were observed and deliberately not reported, having failed the window or threshold test._

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
