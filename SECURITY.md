# Security policy

## Reporting a vulnerability

Report privately through a
[GitHub security advisory](https://github.com/GrahamWallingtonXeroth/moscow-watch/security/advisories/new)
rather than a public issue. You will get an acknowledgement within a few days.

## What this project touches

The threat surface is small and deliberately kept that way:

- **No credentials of any kind.** Every endpoint is public and unauthenticated. There is no
  API key, token, cookie or session anywhere in the codebase, and none is required to run
  it. If you find something that looks like a credential, that is a bug worth reporting.
- **No wallet, no orders, no trading.** The project reads prediction-market prices. It
  cannot place an order, and it holds no keys that would let it.
- **No database, no server.** Output is flat files in a git repository.
- **No code execution from upstream.** Feed and API content is parsed as data. Nothing
  downloaded is executed, rendered as HTML, or used to construct a file path.

Contributors should keep it that way. Treat every upstream response as untrusted input.

## Rate-limit etiquette for third-party APIs

This project depends on free public endpoints run by other people. Being a good guest is a
correctness requirement, not a courtesy:

- **GDELT** documents a limit of one request every five seconds and answers a breach with
  plain text and an HTTP 200. The collector paces itself with a configurable interval whose
  floor is enforced at five seconds by `mw check-config`, and it recognises the throttle
  reply rather than crashing on it. Two broad queries per run, never one per rule.
- **Polymarket, Kalshi and IMF PortWatch** are polled on a six-hourly schedule. Do not
  raise that frequency without a reason; nothing in the data moves fast enough to justify it.
- **Backfill is not a routine operation.** `mw backfill` walks historical endpoints and
  should be run when a market is first tracked, not on every cycle.
- Every request carries an honest, identifying User-Agent with a link back to this
  repository, so an operator who wants to contact us or block us can do either.
- Permanent failures (404, 403, 410) are never retried. 429 responses honour `Retry-After`.

If you are an operator of one of these services and this project is causing you a problem,
open an issue or a security advisory and it will be throttled or removed.

## robots.txt

The project does not fetch anything a site's `robots.txt` disallows for its user agent, does
not rotate or disguise its user agent, does not use logged-in sessions, and does not scrape
paywalled text. `mw doctor --check-robots` re-verifies every configured source against
`urllib.robotparser` on demand.

This is why Reuters is absent: `reuters.com/robots.txt` disallows this agent site-wide. That
is a real cost to the project's coverage, and it is documented rather than worked around.
