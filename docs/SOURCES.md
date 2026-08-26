# Sources

Every endpoint below is **public and unauthenticated**. No API key, token or secret is
required to run any part of this project.

All requests carry an honest, identifying user agent:

```
moscow-watch/0.1 (+https://github.com/GrahamWallingtonXeroth/moscow-watch)
```

The project does not rotate or disguise its user agent, use logged-in sessions, scrape
paywalled text, or fetch anything a site's `robots.txt` disallows.
`mw doctor --check-robots` re-verifies every configured source with `urllib.robotparser`.

Only metadata and short feed-provided summaries are stored. **Complete article bodies are
never fetched or stored.**

## Prediction markets

### Polymarket

| Endpoint | Gives |
| --- | --- |
| `gamma-api.polymarket.com/events?slug=<slug>` | Every leg of a multi-leg event in one call: `question`, `endDate`, `bestBid`, `bestAsk`, `lastTradePrice`, `clobTokenIds` |
| `clob.polymarket.com/prices-history?market=<token>&interval=max&fidelity=60` | Real price history back to market creation |
| `data-api.polymarket.com/trades?market=<conditionId>&limit=N` | The trade tape: real fills with size |

Fetching the whole ladder rather than one leg is the point. A ceasefire market is a set of
dated legs, and reading one of them cannot distinguish a parallel shift in sentiment from a
change in the market's view of timing.

Backfilled records carry `source: "polymarket_prices_history"` so they are always
distinguishable from live collection.

Closed, archived, inactive and past-`endDate` legs are excluded before anything is read
from a ladder. A settled leg that has dropped its prices is skipped rather than being
allowed to fail the whole ladder; a *live* leg whose outcomes and prices do not align is an
error, never a guess.

Terms: [Polymarket documentation](https://docs.polymarket.com/).

### Kalshi

Base `https://external-api.kalshi.com/trade-api/v2`.

| Path | Gives |
| --- | --- |
| `/markets?series_ticker=<T>&status=open` | Markets with `*_dollars` prices (already probabilities, **not** cents) and `*_fp` volume and open interest |
| `/markets/{ticker}/orderbook` | Resting depth |
| `/series/{s}/markets/{t}/candlesticks?start_ts=&end_ts=&period_interval=` | OHLC plus `volume_fp` and `open_interest_fp`. All three parameters are required; interval ∈ {1, 60, 1440} minutes |
| `/events/{event_ticker}` | `settlement_sources` — which live on the **event**, not the market |

Kalshi publishes machine-readable resolution wording. `rules_primary`, `rules_secondary`
and the event's settlement sources are stored verbatim on first sight and diffed on every
run: a change to resolution wording means the same ticker can silently start meaning
something different, which is a material event and appears in `CHANGES.md`.

Tracked series: `KXUSAIRANAGREEMENT`, `KXUSIRANMOU`, `KXWITKOFFRUSSIA`, `KXKASHRUSSIA`,
`KXTRUMPCOUNTRIES`, `KXZELENSKYPUTIN`, `KXPUTINDJTLOCATION`, `KXSANCTIONRUSSIA`,
`KXHOUSERUSSIASANCTION`, `KXHORMUZWEEKLY`, `KXHORMUZAVG`, `KXHORMUZNORM`, `KXBRENTD`.

`KXUSIRANMOU` currently has **no open markets** — the 17 June Islamabad MoU's 60-day window
lapsed on 17 August 2026 and no successor has been listed. It is disabled with that reason
and re-enables if one appears.

**Kalshi has no Ukraine ceasefire, Article 5 or NATO–Russia clash market.** Confirmed by
direct probing of the series endpoint; absence cannot be proved through a ten-result search
endpoint, so it was checked directly. That half of the picture is Polymarket-only.

Kalshi's Hormuz markets settle on **IMF PortWatch**, the same feed collected here directly,
so the market and the counted quantity can be read against each other.

## Counted quantities

### IMF PortWatch

```
services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/Daily_Chokepoints_Data/
  FeatureServer/0/query?where=portid='chokepoint6'&outFields=*&orderByFields=date DESC&f=json
```

Fields: `date`, `n_total`, `n_tanker`, `n_cargo`, `n_container`, `n_dry_bulk`,
`n_general_cargo`, `n_roro`, `capacity_*`. Roughly 2,790 rows of daily history for the
Strait of Hormuz, free.

This is the project's one counted physical quantity: ships, not statements. Two caveats
travel with every reading:

1. **It updates weekly with roughly a week to ten days of lag.** The newest row is never
   today, and the lag is printed beside the value. It is never plotted as if current.
2. **Current counts are extraordinarily low** — single digits per day. That is consistent
   with AIS jamming and dark-vessel behaviour in the strait, which makes this a measure of
   *observed* transits, not of all transits. That is itself a signal, and a reason to state
   the caveat rather than plot the line naively.

Terms: [IMF PortWatch](https://portwatch.imf.org/).

### Russia–Iran contact counter

Not an endpoint — a tally built from the collected corpus. Senior Russia–Iran diplomatic
contacts per fortnight, each stored with its source URL so the count is auditable.

It is the only indicator that separates H3 from H4, and it counts **reported** contacts, so
it is a floor and never a total. It cannot be backfilled: RSS feeds expose only a few days,
so the pre-25-August baseline is not available from any source this project can compliantly
collect. The series starts at first run.

## News

### Independent reporting

`source_family` is the unit of editorial independence, not the domain.

| Source | Feed | Family |
| --- | --- | --- |
| Guardian World | `theguardian.com/world/rss` | `guardian` |
| BBC World | `feeds.bbci.co.uk/news/world/rss.xml` | `bbc` |
| Al Jazeera English | `aljazeera.com/xml/rss/all.xml` | `aljazeera` |
| NPR World | `feeds.npr.org/1004/rss.xml` | `npr` |

### Primary records

Each declares a standpoint, because a statement proves who said it and nothing more.

| Source | Standpoint | State |
| --- | --- | --- |
| The White House | US executive branch | enabled |
| President of Russia (English) | Russian presidential administration | enabled |
| UN News | UN institutional reporting | enabled |
| US Department of State | US State Department | **disabled** — every `state.gov` RSS endpoint returns an HTML error page instead of XML |
| US Treasury / OFAC | US Treasury | **disabled** — press-release RSS returns HTTP 404 and OFAC retired its RSS feed in 2025; only an HTML listing remains |
| NATO | NATO | **disabled** — no discoverable public RSS or Atom endpoint; every advertised path returns HTTP 404 |
| President of Ukraine | Ukrainian presidential administration | **disabled** — `robots.txt` disallows this agent and the endpoint returns HTTP 403 |

All verified 26 August 2026. Reference pages for the disabled four:
[State](https://www.state.gov/press-releases/) ·
[OFAC](https://ofac.treasury.gov/recent-actions) ·
[NATO](https://www.nato.int/cps/en/natohq/news.htm) ·
[Ukraine](https://www.president.gov.ua/en/news)

This is a real gap: with Treasury, State and NATO all unavailable, `official_action` claims
must fall back to two independent newsrooms rather than a primary document.

### Discovery

`api.gdeltproject.org/api/v2/doc/doc` — two broad queries per run, one per theatre.

GDELT is an index, not a witness. Items found only here are typed `discovery_only`, carry a
`discovery:<domain>` family, and are excluded from independence counting by construction. A
discovery hit plus one newsroom is still a single-source lead.

GDELT documents a limit of **one request every five seconds** and answers a breach with
plain text and an HTTP 200, which a naive client treats as malformed JSON. The collector
paces itself, recognises the throttle reply, and runs on a longer timeout because GDELT is
slow and intermittently unavailable. It is non-critical: when it fails, nothing else is
affected, because it never attests anything.

## Why Reuters is absent

Three findings, all verified directly:

1. **GDELT indexes no reuters.com news.** `domain:reuters.com` returns zero articles over
   three days and over a week; over a month it returns one hit, from
   `tax.thomsonreuters.com`, which is not Reuters news.
2. **Reuters disallows this agent site-wide.** `reuters.com/robots.txt` sets, for the
   default group, `Allow: /plus/` then `Disallow: /` — which covers its news sitemap. The
   sitemap is reachable and returns valid XML, but fetching it as a non-allowlisted agent
   would violate the directive.
3. **Google News RSS is also disallowed** (`/rss/` for the default group), and its terms
   restrict the feed to personal, non-commercial feed-reader use.

Reuters is also metered, so article bodies are not reliably machine-readable without a
licence. The only compliant route is the paid **Reuters Connect** licence, which is out of
scope for a keyless public project.

Reuters may still appear as a link when another open source cites it. Nothing here depends
on it, and no document in this repository implies the project read a paywalled article.
