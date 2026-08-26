from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .collectors.contacts import (
    baseline as contact_baseline,
)
from .collectors.contacts import (
    direction as contact_direction,
)
from .collectors.contacts import (
    extract_contacts,
    fortnightly_series,
)
from .collectors.feeds import NewsFeedCollector
from .collectors.gdelt import DISCOVERY_RETRIES, DISCOVERY_TIMEOUT_SECONDS, GdeltDiscovery
from .collectors.kalshi import KalshiCollector, rules_changes
from .collectors.polymarket import PolymarketCollector, open_legs, tape_summary
from .collectors.portwatch import PortWatchCollector, lag_days, rolling_mean
from .config import Config, load_config, validate_config
from .diff import count_suppressed, find_movements
from .diff import render as render_changes
from .health import SourceHealth
from .http import USER_AGENT, HttpClient, HttpError
from .models import utc_now_iso
from .store import JsonlStore
from .tracker import Reading, format_value
from .tracker import render as render_tracker

DEFAULT_CONFIG = "indicators.toml"
DEFAULT_DATA = "data"
DEFAULT_HEALTH = "data/source_status.json"


def _error(exc: Exception) -> tuple[str, str]:
    if isinstance(exc, HttpError):
        return exc.category, str(exc)
    return type(exc).__name__.casefold(), str(exc)


def _load(args: argparse.Namespace) -> tuple[Config, JsonlStore]:
    config = load_config(args.config)
    errors = validate_config(config)
    if errors:
        raise ValueError("invalid config:\n" + "\n".join(f"- {e}" for e in errors))
    return config, JsonlStore(args.data_dir)


# ---------------------------------------------------------------------------
# Collection
# ---------------------------------------------------------------------------


def _collect_polymarket(
    config: Config, store: JsonlStore, health: SourceHealth, client: HttpClient, at: str
) -> list[Reading]:
    collector = PolymarketCollector(client)
    readings: list[Reading] = []
    all_legs: list[dict[str, Any]] = []
    today = datetime.now(UTC).date()

    for indicator in config.indicators_for("polymarket"):
        try:
            legs = collector.ladder(indicator.event_slug, captured_at=at)
            live = open_legs(legs, today=today)
            all_legs.extend(leg.to_dict() for leg in legs)
            if not live:
                raise ValueError("no open legs")
            # For a ladder, headline the leg closest to the indicator's own resolution
            # date when one is configured; otherwise the nearest open leg. Reporting a
            # ladder's nearest rung as "the" price is how a term structure gets misread.
            target = indicator.resolves_date
            front = (
                min(live, key=lambda leg: abs(((leg.resolves or today) - target).days))
                if target
                else live[0]
            )
            value = front.yes_price
            detail = "; ".join(
                f"{(leg.resolves.isoformat() if leg.resolves else '?')}: "
                f"{format_value(indicator, leg.yes_price)}"
                for leg in live
            )
            readings.append(
                Reading(
                    indicator_id=indicator.id,
                    name=indicator.name,
                    source="polymarket",
                    kind=indicator.kind,
                    value=value,
                    display=(
                        f"{format_value(indicator, value)}"
                        f" ({front.group_item_title or (front.resolves.isoformat() if front.resolves else 'front')} leg)"
                    ),
                    collected_at=at,
                    resolves=(front.resolves.isoformat() if front.resolves else indicator.resolves),
                    detail=f"{len(live)} open legs — {detail}",
                    source_url=front.source_url,
                    components=[leg.to_dict() for leg in live],
                )
            )
            health.record_success(
                f"polymarket:{indicator.id}", kind="polymarket", label=indicator.name,
                target=indicator.event_slug, records=len(live), at=at, source_family="polymarket",
            )
        except Exception as exc:
            category, message = _error(exc)
            readings.append(
                Reading(
                    indicator_id=indicator.id, name=indicator.name, source="polymarket",
                    kind=indicator.kind, value=None, display="n/a", collected_at=at,
                    resolves=indicator.resolves, available=False, unavailable_reason=message[:160],
                )
            )
            health.record_failure(
                f"polymarket:{indicator.id}", kind="polymarket", label=indicator.name,
                target=indicator.event_slug, category=category, message=message, at=at,
                source_family="polymarket",
            )
            print(f"WARN polymarket/{indicator.id}: {message[:160]}", file=sys.stderr)

    print(f"polymarket legs added: {store.append_unique('polymarket_legs', all_legs)}")
    return readings


def _collect_kalshi(
    config: Config, store: JsonlStore, health: SourceHealth, client: HttpClient, at: str
) -> tuple[list[Reading], list[dict[str, Any]]]:
    collector = KalshiCollector(client)
    readings: list[Reading] = []
    fresh: list[dict[str, Any]] = []

    for indicator in config.indicators_for("kalshi"):
        try:
            markets = collector.series(indicator.series_ticker, captured_at=at)
            rows = [m.to_dict() for m in markets]
            fresh.extend(rows)
            priced = [m for m in markets if m.last_price is not None or m.yes_bid is not None]
            if not priced:
                raise ValueError("series has no priced open markets")
            # Nearest close is the most decision-relevant leg.
            front = min(priced, key=lambda m: m.close_time or "9999")
            value = front.last_price if front.last_price is not None else front.yes_bid
            readings.append(
                Reading(
                    indicator_id=indicator.id, name=indicator.name, source="kalshi",
                    kind=indicator.kind, value=value,
                    display=format_value(indicator, value), collected_at=at,
                    resolves=str(front.close_time or "")[:10] or indicator.resolves,
                    detail=(
                        f"{len(markets)} open markets; front leg {front.ticker}, "
                        f"open interest {front.open_interest or 0:,.0f}, "
                        f"settles on {', '.join(front.settlement_sources) or 'unstated source'}"
                    ),
                    source_url=front.source_url,
                    components=rows,
                )
            )
            health.record_success(
                f"kalshi:{indicator.id}", kind="kalshi", label=indicator.name,
                target=indicator.series_ticker, records=len(markets), at=at, source_family="kalshi",
            )
        except Exception as exc:
            category, message = _error(exc)
            readings.append(
                Reading(
                    indicator_id=indicator.id, name=indicator.name, source="kalshi",
                    kind=indicator.kind, value=None, display="n/a", collected_at=at,
                    resolves=indicator.resolves, available=False, unavailable_reason=message[:160],
                )
            )
            health.record_failure(
                f"kalshi:{indicator.id}", kind="kalshi", label=indicator.name,
                target=indicator.series_ticker, category=category, message=message, at=at,
                source_family="kalshi",
            )
            print(f"WARN kalshi/{indicator.id}: {message[:160]}", file=sys.stderr)

    previous = store.read("kalshi_markets")
    changes = rules_changes(previous, fresh)
    print(f"kalshi markets added: {store.append_unique('kalshi_markets', fresh)}")
    if changes:
        store.append_unique(
            "kalshi_rules_changes",
            [{**c, "id": f"{c['kind']}:{c['ticker']}:{at}", "detected_at": at} for c in changes],
        )
        print(f"kalshi resolution/listing changes: {len(changes)}")
    return readings, changes


def _collect_portwatch(
    config: Config, store: JsonlStore, health: SourceHealth, client: HttpClient, at: str
) -> list[Reading]:
    collector = PortWatchCollector(client)
    readings: list[Reading] = []
    for indicator in config.indicators_for("portwatch"):
        try:
            rows = [r.to_dict() for r in collector.chokepoint(indicator.chokepoint_id, limit=400)]
            if not rows:
                raise ValueError("no rows returned")
            store.append_unique("portwatch_daily", rows)
            mean = rolling_mean(rows, indicator.value_field or "n_total", window=7)
            lag = lag_days(rows)
            newest = rows[-1]
            readings.append(
                Reading(
                    indicator_id=indicator.id, name=indicator.name, source="portwatch",
                    kind=indicator.kind, value=mean,
                    display=f"{mean:.1f} ships/day (7-day mean)" if mean is not None else "n/a",
                    collected_at=at, unit="ships/day",
                    resolves=indicator.resolves,
                    detail=(
                        f"newest observation {newest['date']}, {lag} days ago — "
                        "this feed lags by roughly a week, so it is never today; "
                        "counts are observed transits, not all transits"
                    ),
                    source_url="https://portwatch.imf.org/",
                    components=rows[-14:],
                )
            )
            health.record_success(
                f"portwatch:{indicator.id}", kind="portwatch", label=indicator.name,
                target=indicator.chokepoint_id, records=len(rows), at=at, source_family="portwatch",
            )
        except Exception as exc:
            category, message = _error(exc)
            readings.append(
                Reading(
                    indicator_id=indicator.id, name=indicator.name, source="portwatch",
                    kind=indicator.kind, value=None, display="n/a", collected_at=at,
                    available=False, unavailable_reason=message[:160],
                )
            )
            health.record_failure(
                f"portwatch:{indicator.id}", kind="portwatch", label=indicator.name,
                target=indicator.chokepoint_id, category=category, message=message, at=at,
                source_family="portwatch",
            )
            print(f"WARN portwatch/{indicator.id}: {message[:160]}", file=sys.stderr)
    return readings


def _collect_feeds(
    config: Config, store: JsonlStore, health: SourceHealth, client: HttpClient, at: str
) -> None:
    collector = NewsFeedCollector(client)
    corpus: list[dict[str, Any]] = []
    kinds = {
        "independent_reporting": "independent_reporting",
        "primary_record": "primary_record",
    }
    for source in config.news_sources:
        kind = kinds.get(source.source_type, "independent_reporting")
        if not source.enabled:
            health.record_disabled(
                f"{kind}:{source.id}", kind=kind, label=source.title,
                target=source.reference_url or source.url, reason=source.disabled_reason,
                source_family=source.source_family,
            )
            continue
        try:
            items = collector.collect(source, window_hours=config.news_timespan_hours)
            corpus.extend(i.to_dict() for i in items)
            health.record_success(
                f"{kind}:{source.id}", kind=kind, label=source.title, target=source.url,
                records=len(items), at=at, source_family=source.source_family,
            )
        except Exception as exc:
            category, message = _error(exc)
            health.record_failure(
                f"{kind}:{source.id}", kind=kind, label=source.title, target=source.url,
                category=category, message=message, at=at, source_family=source.source_family,
            )
            print(f"WARN {kind}/{source.id}: {message[:160]}", file=sys.stderr)
    print(f"corpus items added: {store.append_unique('corpus', corpus)}")


def _collect_discovery(config: Config, store: JsonlStore, health: SourceHealth, at: str) -> None:
    discovery = GdeltDiscovery(
        HttpClient(timeout=DISCOVERY_TIMEOUT_SECONDS, retries=DISCOVERY_RETRIES),
        min_interval=config.discovery_min_interval_seconds,
    )
    found: list[dict[str, Any]] = []
    for query in config.enabled_discovery:
        try:
            items = discovery.collect(query, window_hours=config.news_timespan_hours)
            found.extend(i.to_dict() for i in items)
            health.record_success(
                f"discovery:{query.id}", kind="discovery", label=query.title,
                target="GDELT DOC 2.0", records=len(items), at=at, source_family="gdelt",
            )
        except Exception as exc:
            category, message = _error(exc)
            health.record_failure(
                f"discovery:{query.id}", kind="discovery", label=query.title,
                target="GDELT DOC 2.0", category=category, message=message, at=at,
                source_family="gdelt",
            )
            print(f"WARN discovery/{query.id}: {message[:160]}", file=sys.stderr)
    print(f"discovery leads added: {store.append_unique('discovery', found)}")


def _contact_reading(config: Config, store: JsonlStore, at: str) -> list[Reading]:
    indicators = config.indicators_for("corpus")
    if not indicators:
        return []
    indicator = indicators[0]
    corpus = store.read("corpus")
    contacts = [c.to_dict() for c in extract_contacts(corpus)]
    store.append_unique("contacts", contacts)

    stored = store.read("contacts")
    series = fortnightly_series(stored, anchor=config.contact_anchor)
    store.append_unique(
        "contact_series",
        [{**b, "id": f"fortnight:{b['fortnight_start']}"} for b in series],
    )
    base = contact_baseline(series, before=config.event_date)
    latest = series[-1] if series else None
    heading = contact_direction(series, base)

    return [
        Reading(
            indicator_id=indicator.id,
            name=indicator.name,
            source="corpus",
            kind=indicator.kind,
            value=float(latest["count"]) if latest else None,
            display=(f"{latest['count']} reported contacts this fortnight" if latest else "n/a"),
            collected_at=at,
            unit="contacts/fortnight",
            detail=(
                f"direction vs pre-{config.event_date.isoformat()} baseline: {heading}; "
                f"baseline {base.get('mean_per_fortnight')} per fortnight over "
                f"{base.get('fortnights')} fortnights; counts REPORTED contacts only, "
                "so this is a floor and never a total"
            ),
            components=series[-6:],
        )
    ]


def command_collect(args: argparse.Namespace) -> int:
    config, store = _load(args)
    health = SourceHealth(args.health_output)
    client = HttpClient(timeout=args.timeout)
    at = utc_now_iso()
    readings: list[Reading] = []

    if args.source in {"all", "markets"}:
        readings += _collect_polymarket(config, store, health, client, at)
        readings += _collect_kalshi(config, store, health, client, at)[0]
    if args.source in {"all", "portwatch"}:
        readings += _collect_portwatch(config, store, health, client, at)
    if args.source in {"all", "feeds"}:
        _collect_feeds(config, store, health, client, at)
    if args.source in {"all", "discovery"}:
        _collect_discovery(config, store, health, at)
    if args.source in {"all", "feeds"}:
        readings += _contact_reading(config, store, at)

    rows = [r.to_dict() for r in readings]
    for row in rows:
        row["id"] = f"{row['indicator_id']}:{row['collected_at']}"
    print(f"indicator readings added: {store.append_unique('readings', rows)}")

    document = health.write(config.stale_after_hours)
    summary = document["summary"]
    print(f"source health: {summary['overall']}")
    if summary["overall"] == "unavailable" and not args.allow_partial:
        return 1
    return 0


def command_backfill(args: argparse.Namespace) -> int:
    """Real historical prices, so a baseline never has to be invented."""
    config, store = _load(args)
    collector = PolymarketCollector(HttpClient(timeout=args.timeout))
    today = datetime.now(UTC).date()
    points = 0
    trades = 0

    for indicator in config.indicators_for("polymarket"):
        try:
            legs = open_legs(collector.ladder(indicator.event_slug), today=today)
        except Exception as exc:
            print(f"WARN backfill/{indicator.id}: {_error(exc)[1][:150]}", file=sys.stderr)
            continue
        for leg in legs:
            token = leg.token_for("Yes")
            if token:
                try:
                    history = collector.history(
                        token, market_id=leg.market_id, fidelity=args.fidelity
                    )
                    points += store.append_unique(
                        "polymarket_history", [p.to_dict() for p in history]
                    )
                except Exception as exc:
                    print(f"WARN history/{leg.market_slug}: {_error(exc)[1][:120]}", file=sys.stderr)
            if args.trades and leg.condition_id:
                try:
                    tape = collector.trades(
                        leg.condition_id, market_id=leg.market_id, limit=args.trade_limit
                    )
                    trades += store.append_unique(
                        "polymarket_trades", [t.to_dict() for t in tape]
                    )
                except Exception as exc:
                    print(f"WARN trades/{leg.market_slug}: {_error(exc)[1][:120]}", file=sys.stderr)

    print(f"history points added: {points}")
    if args.trades:
        summary = tape_summary(store.read("polymarket_trades"))
        print(f"trades added: {trades} | tape: {summary}")
    return 0


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _latest_readings(store: JsonlStore) -> list[Reading]:
    latest: dict[str, dict[str, Any]] = {}
    for row in store.read("readings"):
        key = str(row.get("indicator_id"))
        if key not in latest or str(row.get("collected_at", "")) > str(
            latest[key].get("collected_at", "")
        ):
            latest[key] = row
    known = {f.name for f in Reading.__dataclass_fields__.values()}
    return [Reading(**{k: v for k, v in row.items() if k in known}) for row in latest.values()]


def command_tracker(args: argparse.Namespace) -> int:
    config, store = _load(args)
    health_path = Path(args.health_output)
    health = (
        SourceHealth(health_path).document(config.stale_after_hours)
        if health_path.exists()
        else {}
    )
    readings = _latest_readings(store)
    Path(args.output).write_text(
        render_tracker(config, readings, health=health), encoding="utf-8"
    )
    print(f"wrote {args.output} ({len(readings)} indicators)")
    return 0


def command_diff(args: argparse.Namespace) -> int:
    config, store = _load(args)
    history = store.read("readings")
    since = args.since or (
        datetime.now(UTC) - timedelta(days=7)
    ).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    movements = find_movements(config, history, since=since)
    suppressed = count_suppressed(config, history, since=since)
    changes = [
        c for c in store.read("kalshi_rules_changes")
        if str(c.get("detected_at", "")) >= since
    ]
    Path(args.output).write_text(
        render_changes(config, movements, since=since, rules_changes=changes, suppressed=suppressed),
        encoding="utf-8",
    )
    print(
        f"wrote {args.output} ({len(movements)} movements, {suppressed} suppressed, "
        f"{len(changes)} listing/wording changes)"
    )
    return 0


def command_charts(args: argparse.Namespace) -> int:
    config, store = _load(args)
    try:
        from . import charts
    except ImportError as exc:
        print(f"charts require matplotlib: {exc}", file=sys.stderr)
        return 1
    written = charts.render_all(config, store, out_dir=Path(args.out_dir))
    for path in written:
        print(f"wrote {path}")
    return 0


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------


def command_check(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    errors = validate_config(config)
    if errors:
        print("\n".join(f"- {e}" for e in errors), file=sys.stderr)
        return 1
    tracked = [h for h in config.hypotheses if h.scored]
    print(
        f"OK: {len(tracked)} tracked hypotheses ({len(config.hypotheses) - len(tracked)} noted) | "
        f"{len(config.enabled_indicators)}/{len(config.indicators)} indicators | "
        f"{len(config.reporting_families)} independent reporting families | "
        f"{len(config.enabled_discovery)} discovery queries | "
        f"{len(config.claim_rules)} claim rules"
    )
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    errors = validate_config(config)
    if errors:
        print("\n".join(f"- {e}" for e in errors), file=sys.stderr)
        return 1
    client = HttpClient(timeout=args.timeout)
    fatal: list[str] = []
    print(f"user-agent: {USER_AGENT}\n")

    print("Polymarket")
    pm = PolymarketCollector(client)
    pm_ok = 0
    for indicator in config.indicators_for("polymarket"):
        try:
            live = open_legs(pm.ladder(indicator.event_slug))
            pm_ok += 1
            print(f"  ok       {indicator.id:<30} {len(live)} open legs")
        except Exception as exc:
            print(f"  FAIL     {indicator.id:<30} {_error(exc)[1][:100]}", file=sys.stderr)
    if pm_ok == 0 and config.indicators_for("polymarket"):
        fatal.append("no Polymarket indicator is reachable")

    print("\nKalshi")
    ks = KalshiCollector(client)
    ks_ok = 0
    for indicator in config.indicators_for("kalshi"):
        try:
            markets = ks.series(indicator.series_ticker, with_settlement_sources=False)
            ks_ok += 1
            print(f"  ok       {indicator.id:<30} {len(markets)} open markets")
        except Exception as exc:
            print(f"  FAIL     {indicator.id:<30} {_error(exc)[1][:100]}", file=sys.stderr)
    if ks_ok == 0 and config.indicators_for("kalshi"):
        fatal.append("no Kalshi indicator is reachable")

    print("\nIMF PortWatch (counted quantity)")
    pw = PortWatchCollector(client)
    pw_ok = 0
    for indicator in config.indicators_for("portwatch"):
        try:
            rows = [r.to_dict() for r in pw.chokepoint(indicator.chokepoint_id, limit=30)]
            pw_ok += 1
            print(
                f"  ok       {indicator.id:<30} {len(rows)} rows, newest {rows[-1]['date']} "
                f"({lag_days(rows)} days ago)"
            )
        except Exception as exc:
            print(f"  FAIL     {indicator.id:<30} {_error(exc)[1][:100]}", file=sys.stderr)
    if pw_ok == 0 and config.indicators_for("portwatch"):
        fatal.append("the only counted-quantity source is unreachable")

    print("\nFeeds")
    feeds = NewsFeedCollector(client)
    families: set[str] = set()
    for source in config.news_sources:
        if not source.enabled:
            print(f"  disabled {source.id:<30} {source.disabled_reason[:70]}")
            continue
        try:
            items = feeds.collect(source, window_hours=config.news_timespan_hours)
            if source.source_type == "independent_reporting":
                families.add(source.source_family)
            print(f"  ok       {source.id:<30} {len(items)} items")
        except Exception as exc:
            print(f"  warn     {source.id:<30} {_error(exc)[1][:100]}")
    if len(families) < 2:
        fatal.append(
            f"only {len(families)} independent reporting family/families reachable; "
            "nothing can be corroborated"
        )

    print("\nDiscovery (GDELT — leads only, never promotes a claim)")
    gd = GdeltDiscovery(HttpClient(timeout=DISCOVERY_TIMEOUT_SECONDS, retries=DISCOVERY_RETRIES))
    gd_ok = 0
    for query in config.enabled_discovery:
        try:
            items = gd.collect(query, window_hours=config.news_timespan_hours)
            gd_ok += 1
            print(f"  ok       {query.id:<30} {len(items)} leads")
        except Exception as exc:
            print(f"  warn     {query.id:<30} {_error(exc)[1][:100]}")

    if args.check_robots:
        print("\nRobots compliance")
        import urllib.robotparser as robotparser

        for source in config.enabled_news_sources:
            parts = urlparse(source.url)
            parser = robotparser.RobotFileParser()
            parser.set_url(f"{parts.scheme}://{parts.netloc}/robots.txt")
            try:
                parser.read()
                allowed = parser.can_fetch(USER_AGENT, source.url)
            except Exception:
                allowed = "unreadable"
            if allowed is False:
                fatal.append(f"{source.id} is disallowed by robots.txt")
            print(f"  {'ok      ' if allowed is True else 'CHECK   '} {source.id:<30} {allowed}")

    print("\nRedundancy")
    print(f"  polymarket indicators reachable : {pm_ok}")
    print(f"  kalshi indicators reachable     : {ks_ok}")
    print(f"  counted-quantity sources        : {pw_ok}")
    print(f"  independent reporting families  : {len(families)} ({', '.join(sorted(families)) or 'none'})")
    print(f"  discovery queries reachable     : {gd_ok} (non-critical)")

    if fatal:
        print("\nFAILED:")
        for item in fatal:
            print(f"  - {item}")
        return 1
    print("\nPASSED")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mw",
        description="Collect and publish indicators bearing on the August 2026 Moscow visit.",
    )
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--data-dir", default=DEFAULT_DATA)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--health-output", default=DEFAULT_HEALTH)
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check-config", help="validate indicators.toml offline")
    check.set_defaults(handler=command_check)

    doctor = sub.add_parser("doctor", help="read-only live checks; writes nothing")
    doctor.add_argument("--check-robots", action="store_true")
    doctor.set_defaults(handler=command_doctor)

    collect = sub.add_parser("collect", help="collect from every configured source")
    collect.add_argument(
        "--source", choices=("all", "markets", "portwatch", "feeds", "discovery"), default="all"
    )
    collect.add_argument("--allow-partial", action="store_true")
    collect.set_defaults(handler=command_collect)

    backfill = sub.add_parser("backfill", help="real Polymarket history and trade tape")
    backfill.add_argument("--fidelity", type=int, default=1440, help="minutes per point")
    backfill.add_argument("--trades", action="store_true", help="also fetch the trade tape")
    backfill.add_argument("--trade-limit", type=int, default=500)
    backfill.set_defaults(handler=command_backfill)

    tracker = sub.add_parser("tracker", help="render TRACKER.md")
    tracker.add_argument("--output", default="TRACKER.md")
    tracker.set_defaults(handler=command_tracker)

    diff = sub.add_parser("diff", help="render CHANGES.md")
    diff.add_argument("--since", default=None, help="ISO timestamp; defaults to 7 days ago")
    diff.add_argument("--output", default="CHANGES.md")
    diff.set_defaults(handler=command_diff)

    charts = sub.add_parser("charts", help="regenerate the committed PNGs")
    charts.add_argument("--out-dir", default="assets")
    charts.set_defaults(handler=command_charts)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        status = args.handler(args)
    except (ValueError, OSError, HttpError) as exc:
        print(str(exc), file=sys.stderr)
        status = 2
    raise SystemExit(status)
