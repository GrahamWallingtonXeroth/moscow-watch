# Contributing

Contributions are welcome from developers, forecasters, regional specialists and sceptical
readers. Disagreement about what the evidence means is the point of the project.

## The one rule everything else follows from

> **The repo collects and publishes. It does not render verdicts.**

Pull requests that add scoring, ranking, weighting, an aggregate "which hypothesis is
winning" number, or a position-pricing calculation will be declined however well
implemented. A previous version had all of those and they made it look more rigorous than
it was.

Interpretation goes in the article, with a name attached to it.

## Standing rules

- **Nothing appears in `TRACKER.md` that was not collected from a named source.** No
  placeholders, no illustrative values, no defaults standing in for data. Do not commit
  hand-authored rows to `data/`; if you need example data, put it in `tests/fixtures/`.
- **If a collector fails, its row says so.** It never falls back to a stale value silently.
- **Every claim in the README about what the code does must be true of the code as pushed.**
  If you cannot make something work, delete the claim rather than the test.
- **Prefer deleting a feature to shipping one that looks more rigorous than it is.**

## Adding a source

Any new source must:

- be public and keyless — no paid services, API keys, secrets or databases;
- be permitted by its own `robots.txt` for this project's user agent, verified with
  `mw doctor --check-robots`;
- be fetched with the honest project user agent, never a disguised or rotated one, and
  never through a logged-in session or a paywall;
- be fetched **once per run**, with rules applied locally afterwards;
- declare a `source_type` and a `source_family`, plus a `standpoint` if it is a primary
  record;
- fail with a readable error rather than half-parsing the wrong content type.

If a source cannot be collected compliantly, disable it in `indicators.toml` with a stated
reason and a reference link, and say so in `docs/SOURCES.md`. Publishing "unavailable,
official page linked" is better than committing a dead URL.

### Choosing a source family

`source_family` is the unit of editorial independence, **not the domain**. Two regional
editions of one newsroom, or two outlets syndicating the same wire copy, must share a
family. Getting this wrong is the easiest way to make corroboration meaningless: two
"independent" sources that are really one produce an attested claim from a single report.

### GDELT stays a discovery index

Do not make GDELT results attestable and do not add per-rule GDELT queries. It exists to
surface stories no configured feed carried. If a lead matters, add a source that reports it
directly rather than lowering the bar.

## Adding an indicator

Every indicator needs a `resolves` date where one exists, a `material_move` fixed in
advance, and at least one `bears_on` entry. An indicator that discriminates between no
hypotheses should not be tracked.

Choose `material_move` **before** looking at how the series has moved. A threshold picked
after seeing the data is not a threshold.

## Adding a hypothesis

It needs a falsifier and a date. Anything without one is a narrative, not a hypothesis, and
belongs in the noted-and-not-tracked set with an explanation — as H7 is.

## Development

```bash
python -m venv .venv && . .venv/bin/activate
python -m pip install -e ".[charts]" ruff

ruff check src tests
python -m unittest discover -s tests -v
mw check-config
mw doctor --check-robots
```

**Tests must not touch the network.** Use fixtures and the fakes in `tests/support.py`; the
fake HTTP client deliberately applies the same content-type checks as the real one, so a
fake cannot pass a check the real client would fail.

## Pull requests

A source-code change should include a test.

A change to a source family, claim rule, indicator threshold or hazard calculation must
include:

1. The reason for the change.
2. **Whether you had already seen the outcome the change would affect.**
3. The effect on the current `TRACKER.md`.

Point 2 is the one that matters. A threshold adjusted after seeing the result it governs is
no longer fixed in advance, and the project loses the only thing that makes it worth
reading.

## Please do not commit

Secrets, cookies or credentials; complete copyrighted article bodies; personal data; claims
about the identity or motives of individual traders; or a local virtual environment.
