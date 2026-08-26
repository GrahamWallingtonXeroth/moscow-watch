# Moscow Watch

[![Test](https://github.com/GrahamWallingtonXeroth/moscow-watch/actions/workflows/test.yml/badge.svg)](https://github.com/GrahamWallingtonXeroth/moscow-watch/actions/workflows/test.yml)
[![Update watch](https://github.com/GrahamWallingtonXeroth/moscow-watch/actions/workflows/watch.yml/badge.svg)](https://github.com/GrahamWallingtonXeroth/moscow-watch/actions/workflows/watch.yml)

**On 25 August 2026 the director of the CIA spent about seven and a half hours in Moscow.
Nobody has reported what was discussed.**

This repository does not tell you why he went. It collects the quantities that would move
differently depending on the answer, publishes them with their provenance and their
resolution dates, and leaves the interpreting to a named human in an article.

That division is the whole design:

> **The repo collects and publishes. It does not render verdicts.**

There are no consistency scores, no weighted evidence totals, no profit-and-loss tables
and no automated adjudication of which hypothesis is winning. Those things create the appearance of rigour
while adding nothing a reader can check.

- **[TRACKER.md](TRACKER.md)** — every indicator, its current value, when it was collected,
  and when it becomes decidable. Opens with the resolution calendar.
- **[CHANGES.md](CHANGES.md)** — what moved since the last run, and by how much.

![What the market thinks about the timing of a Ukraine deal](assets/hazard-curve.png)

## The six hypotheses

Each states, in advance, what would falsify it and by when. Committing to that before the
evidence arrives is the only thing separating a tracker from a narrative.

| | Hypothesis | The claim | Falsifier | By |
| --- | --- | --- | --- | --- |
| **H1** | Uranium custody | A disposition route, through Moscow, for Iran's unaccounted enriched uranium — reviving the 2015 mechanism | No IAEA, Rosatom or US statement referencing third-party custody, transfer or accounting of Iranian material | 31 Oct 2026 |
| **H2** | Ukraine endgame | Preparation for a settlement or a Trump–Putin meeting, explored deniably because the formal track has been suspended since February | No announced meeting, no resumed trilateral track, and no near-dated change in the ceasefire term structure | 31 Oct 2026 |
| **H3** | Iran-for-Ukraine bargain | Reciprocal costly concessions: US room in Ukraine, Russian pullback from Iran | Continued or increased Russian engagement with Tehran alongside continued US costs on Russia | 30 Nov 2026 |
| **H4** | Brokerage | Washington asked Moscow to carry messages to Tehran — an *increase* in Russian engagement, at American request | A fall in reported Russia–Iran contacts below the pre-25-August baseline, sustained | 31 Oct 2026 |
| **H5** | Warning | A demand about Russian intelligence support to Iranian forces targeting American assets. Coercion, not cooperation | No new US costs on Russia and no reported reduction in targeting support | 31 Oct 2026 |
| **H6** | Channel maintenance | Ordinary service business: prisoners, counterterrorism, embassies. There is no US ambassador in Moscow | Any documented substantive outcome on Iran, uranium or Ukraine attributable to the visit | 31 Oct 2026 |

**H7, arms control, is named and deliberately not tracked.** New START expired on
5 February 2026 with no successor and no strategic stability talks exist, which makes it a
plausible reason to send an intelligence chief. But no outlet has reported it as an agenda
item and **there is no prediction market on arms control on either venue**, so there is
nothing to test it against. An untestable hypothesis should be named and set aside, not
quietly promoted to a testable one. If a market on a New START successor appears, it moves
into the tracked set.

### Why the discriminator map matters

H3 and H4 produce nearly identical *Iran* outcomes — a pause, resumed talks, a softer
nuclear posture. Commentary will read either as "Russia helped". They are opposite in
mechanism and opposite in what they cost America, and the thing that separates them is
simply **which direction Russian officials are travelling**.

![Six explanations, two axes we can count](assets/discriminator-map.png)

The marker's position must be derivable from the ledger. When it is not — as now, because
the contact counter has no pre-event baseline — it is drawn as an empty ring at centre and
labelled *not yet determined*, never guessed.

## Where every number comes from

All endpoints are public and require **no authentication, no API key and no secret**.

| Source | What it gives | Endpoint |
| --- | --- | --- |
| Polymarket Gamma | Full event ladders in one call, bid/ask, CLOB token ids | `gamma-api.polymarket.com/events?slug=` |
| Polymarket CLOB | Real price history back to market creation | `clob.polymarket.com/prices-history` |
| Polymarket data-api | The trade tape — size, not just price | `data-api.polymarket.com/trades` |
| Kalshi | Markets, order books, candlesticks **with open interest**, and machine-readable resolution wording | `external-api.kalshi.com/trade-api/v2` |
| IMF PortWatch | Daily Strait of Hormuz transits, ~2,790 rows of history | `services9.arcgis.com/.../Daily_Chokepoints_Data` |
| RSS | Guardian, BBC, Al Jazeera, NPR, White House, Kremlin, UN News | publisher feeds |
| GDELT | Discovery only — candidate leads it may never promote | `api.gdeltproject.org/api/v2/doc/doc` |

Two things about that table are worth pausing on.

**The trade tape matters more than it sounds.** It is the difference between "traders
repriced the war" and "someone bought $400 of a thin market after reading a headline", and
no commentary on prediction markets ever checks it. On the ceasefire ladder the median
trade is currently under $15.

**Kalshi's Hormuz market settles on IMF PortWatch** — the same feed collected here
directly, so the market and the counted quantity can be read against each other.

### Reading a ladder instead of a price

A ceasefire market prices "a deal by date D" for several D. Those raw numbers rise with
time simply because a longer window contains more chances. Converting each rung to a
*forward conditional hazard* strips that out and makes the rungs comparable.

The point is not the level, it is the **shape**: a parallel shift is sentiment, a change in
shape is news about timing. Watching only the December leg cannot tell them apart. The
formula is in [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## What this project explicitly does not do

- **It does not say which hypothesis is winning.** No score, no ranking, no aggregate.
- **It does not price positions.** No profit-and-loss tables, no return calculations, and
  no claim about whether any market is mispriced. Earlier versions did all three, and the
  numbers looked more rigorous than they were.
- **It does not treat a source saying something as that thing being true.** A claim is
  labelled by how well it is attested — `primary_documented`, `corroborated`,
  `single_source`, `contested`, `discovery_only` — and the label is the whole output.
- **It does not let an index vote.** A GDELT hit is a pointer to a story, not a witness to
  it, and can never be the second source that attests a claim.
- **It does not invent history.** If two real observations do not exist, the tracker says
  so rather than assuming a baseline.

## Known gaps, stated here rather than in a subpage

- **No arms-control market exists on either venue**, so H7 is untestable by design.
- **Kalshi has no Ukraine ceasefire, Article 5 or NATO–Russia clash market.** Confirmed by
  direct probing. That half of the picture is Polymarket-only.
- **Reuters cannot be collected.** `reuters.com/robots.txt` disallows all automated access
  for this agent, and GDELT indexes no reuters.com news. The only compliant route is the
  paid Reuters Connect licence. The corpus is Guardian, BBC, Al Jazeera, NPR and UN News
  plus primary records.
- **Four primary sources are unavailable**, which weakens `official_action` claims: State
  serves HTML instead of XML, Treasury returns 404 with OFAC's RSS retired in 2025, NATO
  publishes no discoverable feed, and `president.gov.ua` disallows this agent.
- **PortWatch lags about a week**, so its newest row is never today. Current Hormuz counts
  are extraordinarily low, consistent with AIS jamming and dark-vessel behaviour: this
  measures *observed* transits, not all transits. That is itself a signal, and a reason not
  to plot the line naively.
- **The contact counter measures *reported* contacts.** Unreported diplomacy is exactly
  what this story is about, so the count is a floor and never a total. It also **cannot be
  backfilled**: RSS feeds expose only a few days, so the pre-25-August baseline the
  discriminator map needs is not available from any source this project can compliantly
  collect. The series starts from first run and accumulates.
- **The far legs of the ceasefire ladder are thin** — the March and June 2027 rungs carry
  under $5,000 of volume between them. Treat the Q1-2027 peak with the caution that
  deserves.
- **Claim matching runs on headlines and feed summaries**, not article bodies. A headline
  can invert the meaning of the article beneath it.

## How to disagree with it

Every number is traceable and every judgement is separable from the data.

- **Think an indicator is wrong?** `indicators.toml` holds every one, with its source, its
  threshold and its stated bearing. Open an issue or a PR against that file.
- **Think a claim was over-attested?** Every claim records the rule that matched it, the
  exact terms, the source families and a citation per supporting article. Check the
  citations.
- **Think the threshold is doing the work?** `material_move` is fixed in advance per
  indicator, and `CHANGES.md` reports how many moves were suppressed by it.
- **Think the hazard maths is wrong?** It is forty lines in `src/moscow_watch/hazard.py`
  with the degenerate cases tested. Recompute it.
- **Think a hypothesis is missing?** Add it with a falsifier and a date. Anything without
  one does not belong in the tracked set.

## Running it

```bash
python -m venv .venv && . .venv/bin/activate
python -m pip install -e ".[charts]"

mw check-config              # validate indicators.toml offline
mw doctor --check-robots     # read-only live checks; writes nothing
mw collect --allow-partial   # collect from every configured source
mw backfill --trades         # real price history and the trade tape
mw tracker                   # render TRACKER.md
mw diff --since 2026-08-25   # render CHANGES.md
mw charts                    # regenerate both PNGs
```

The collectors, tracker and diff use only the standard library. `matplotlib` is needed for
the charts and nothing else.

```text
indicators.toml              hypotheses, indicators, sources, resolution dates
src/moscow_watch/
  collectors/                polymarket · kalshi · portwatch · contacts · feeds · gdelt
  corroboration.py           attestation taxonomy — labels, never numbers
  dedupe.py                  syndication clustering
  hazard.py                  term-structure maths
  tracker.py                 renders TRACKER.md
  diff.py                    renders CHANGES.md
  charts.py                  renders the committed PNGs
data/*.jsonl                 append-only, collected only
```

Everything in `data/` was written by `mw collect` from a real upstream response. Nothing in
this repository is hand-authored, illustrative or a placeholder standing in for data.

## Licence

MIT. See [LICENSE](LICENSE). Contributions welcome — see
[CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
