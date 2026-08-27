# Methodology

The design constraint, stated plainly:

> **The repo collects and publishes. It does not adjudicate hypotheses.**

No consistency scores, no weighted evidence totals, no profit-and-loss tables, no
automated ranking. The unit
is an **indicator**: a named quantity, from a named source, with a value, a timestamp, a
date on which it becomes decidable, and a stated direction of implication for each
hypothesis. A human does the interpreting, in the article, under their own name.

## Hazard maths

A ceasefire ladder prices "a deal by date D" for several D. Those cumulative numbers rise
with time simply because a longer window contains more chances, so comparing rungs directly
says almost nothing.

For adjacent rungs with cumulative probabilities `p₁` (by `d₁`) and `p₂` (by `d₂`), the
**forward conditional** probability — the chance the event arrives inside that window given
it has not arrived yet — is

```
q = (p₂ − p₁) / (1 − p₁)
```

Treating that as a constant per-day hazard `λ` over `n = d₂ − d₁` days gives

```
λ = −ln(1 − q) / n
```

and the comparable **30-day equivalent** plotted on the chart is

```
1 − exp(−30 λ)
```

Degenerate cases, all tested:

| Case | Behaviour |
| --- | --- |
| `p₁ = 1` | Nothing is left to happen; `q = 0` |
| `p₂ < p₁` (non-monotone ladder) | Clamped to `q = 0` rather than reported as negative. Adjacent legs trade independently, so real quotes are sometimes inverted |
| `q = 1` | `λ` is infinite; the monthly equivalent is capped at 1.0 |
| `n ≤ 0` | Rejected. A rung at or before the anchor date carries no window |
| `p` outside `[0, 1]` | Rejected |

**Legs shorter than 14 days are excluded from the plot.** Their implied hazard is dominated
by the exchange tick size rather than by any belief about timing. They are still computed
and reported, and the exclusion is stated in the chart caption, because silently dropping a
data point is how a chart starts lying.

**Read the shape, not the level.** A parallel shift in the ladder is sentiment. A change in
the shape — a near-dated hump appearing — is news about timing. Watching a single leg cannot
tell them apart.

## Corroboration taxonomy

Finding a story and believing it are different operations.

### Source types

| Type | What it can establish |
| --- | --- |
| `primary_record` | What that institution said or did |
| `independent_reporting` | An external event, with corroboration |
| `discovery_only` | Nothing. It points at stories |

**`source_family` is the unit of editorial independence, not the domain.** Two regional
editions of one newsroom, or two outlets running the same wire copy, share a family and
cannot corroborate each other.

**Every primary record declares a `standpoint`**, and `check-config` rejects one that does
not. A Kremlin statement proves the Kremlin made the statement; it does not make the
contents true, and the record says which is which.

### Claim types and what promotes them

| Claim type | Requirement |
| --- | --- |
| `official_action` | A primary record, or two independent newsrooms |
| `actor_statement` | The actor's own record. Establishes only that they said it |
| `external_observable` | Two editorially independent source families |
| `allegation` | Two editorially independent source families |

### Attestation labels

`primary_documented` · `corroborated` · `single_source` · `contested` · `discovery_only`

**The label is the output.** No number is attached to a claim and nothing is summed.
Single-source, contested and discovery-only items are shown, clearly separated, so a reader
can see what was found and why it fell short.

**Discovery can never attest.** GDELT families are excluded from independence counting by
construction: a discovery hit plus one newsroom is still a single-source lead.

### Counting once

Syndicated copies of one story are clustered by canonical URL and by near-duplicate
headline, using deterministic token shingles with a Jaccard threshold. One story yields one
claim per hypothesis however many outlets carried it and however many rules it trips.
Corroboration must also fall inside the rule's window, so a report from last month cannot
silently corroborate today's.

### Matching

Required keyword groups, all of which must contribute at least one match, on normalised
**whole words or phrases** — `stop` does not match `nonstop`.

**Denials block matches.** A standard negation vocabulary (`denies`, `rejects`, `ruled out`,
`no evidence`, and others) stops a headline reporting a denial being read as a report of the
event. "Moscow denies halting weapons to Iran" is not a halt.

Matching runs on headlines and feed summaries, recorded as `headline and summary rule` on
every claim. This is a real limitation: a headline can invert the article beneath it.

## Change detection

`CHANGES.md` is the feature the follow-up articles are written from, so two suppressions
keep it honest:

- **No move computed over a window shorter than `min_change_window_hours`** (default 6). A
  half-point move over a three-minute window is noise, and reporting it as news is how a
  tracker loses its reader.
- **No move smaller than the indicator's own `material_move`**, fixed in advance in
  `indicators.toml` rather than chosen after seeing the data.

The count of suppressed moves is printed, so the suppression is visible rather than silent.

A change to Kalshi resolution wording, or a new market appearing in a tracked series, is
reported as a material event. The same ticker can silently start meaning something
different, and a chart plotted straight through such a change is misleading. First sighting
of a series is not a change.

## Chart axis definitions

Both markers must be derivable from the ledger. If either axis lacks data the marker is
drawn as an empty ring at centre and labelled *not yet determined* — never guessed.

### X — Russian engagement with Iran

From **Russia–Iran engagement volume (reporting index)**, not from the contact counter. The
counter cannot reach behind 25 August — RSS exposes only a few days — and an axis without a
pre-event baseline cannot be read at all. GDELT does hold history, so the baseline is built
from GDELT DOC 2.0 in `timelinevol` mode by `mw backfill --engagement`, covering 1 January
2026 to 24 August 2026 and bucketed by fortnight.

With `latest` the mean daily volume in the current post-event fortnight and `mean` the mean
across the complete pre-event fortnights:

```
x = clamp( (latest − mean) / mean,  −1, +1 )
```

Negative is *Russia pulls back from Tehran*; positive is *Russia leans in*.

Three limits travel with that number wherever it appears:

1. It counts **reporting volume** from a news index — the share of the coverage GDELT
   monitored that day which matched the query — and **not contacts**. It is a proxy for
   diplomatic tempo, not a tally of meetings.
2. Because it is a share of coverage, **only the direction of change against the baseline
   is meaningful**. The level on its own says nothing.
3. Counting how much a subject is reported and attesting that something happened are
   different operations. This performs the first only. The rule that a GDELT hit can never
   attest a claim is unchanged: nothing in this series promotes or corroborates anything.

Two bucketing rules keep the comparison honest. The baseline uses only **complete**
fortnights that end before 25 August, so a short window is never averaged in beside a full
one and the event's own coverage spike never lands in its own baseline. The live series is
bucketed in 14-day windows measured **from the event date**, so a window never mixes days
before the visit with days after it. And the marker is not placed at all until the current
fortnight holds at least seven days, because half a fortnight is the least that can be
compared with a whole one.

The directly collected contact counter runs alongside this and is unchanged. It counts
**reported** contacts from the collected corpus, each stored with its source URL, so it is
the auditable series; unreported diplomacy is exactly what this story is about, so it is a
floor and never a total.

### Y — US posture toward Russia

From the mean of the collected probabilities for the two sanctions markets
(`kalshi_sanction_russia`, `kalshi_house_russia_sanction`) and the Ukraine security
guarantee market (`pm_ukraine_security_guarantee`), requiring at least two of the three:

```
y = clamp( −(mean − 0.5) × 2,  −1, +1 )
```

Higher sanctions and guarantee odds both mean Washington is imposing costs, so the index is
negated: costs sit low on the axis, relief sits high.

## Source health

Health is a keyed document overwritten in place, not an append-only ledger, so a
permanently broken endpoint updates one row rather than growing the repository. Error
categories are stable strings (`http_404`, `wrong_content_type`, `rate_limited`), so
identical repeated failures stay byte-identical.

Permanent statuses (400, 401, 403, 404, 405, 410, 451) are never retried. 429 honours
`Retry-After`. Everything else uses bounded exponential backoff. Gzip bodies are
decompressed transparently, because a raw gzip stream handed to an XML parser fails in a way
that reads like a broken feed rather than a compressed one.

Losing GDELT does not stop the tracker, because GDELT never attests. Losing the second
independent newsroom does, because nothing can then be corroborated.

## Changing any of this

A change to a threshold, source family, claim rule or hazard calculation requires the
reason, the effect on the current tracker, and **whether the author had already seen the
outcome the change would affect**. A threshold adjusted after seeing the result it governs
is no longer fixed in advance.
