from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from urllib.parse import urlencode, urlparse

from ..config import DiscoveryQuery, timespan_label
from ..http import HttpClient, HttpError
from ..models import NewsItem

GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

# GDELT asks for no more than one request every five seconds and answers a breach with
# plain text rather than JSON, so pacing is part of using it correctly.
MIN_INTERVAL_SECONDS = 6.0

# GDELT routinely takes 5-20s for a broad query. A short timeout turns a healthy but slow
# index into a spurious failure, so discovery gets its own budget. Two queries at two
# attempts each stays comfortably inside the workflow's ten-minute cap.
DISCOVERY_TIMEOUT_SECONDS = 30.0
DISCOVERY_RETRIES = 1

# A timelinevol query spanning months is a much heavier job for GDELT than an article
# list over three days, and it is run rarely and outside the six-hourly schedule, so it
# gets a longer budget. It is still bounded: a hung backfill must fail, not hang.
TIMELINE_TIMEOUT_SECONDS = 120.0
TIMELINE_RETRIES = 3


def _published(value: str) -> str:
    if not value:
        return ""
    for fmt in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S"):
        try:
            return (
                datetime.strptime(value, fmt)
                .replace(tzinfo=UTC)
                .isoformat()
                .replace("+00:00", "Z")
            )
        except ValueError:
            continue
    return ""


# The rate limit belongs to the endpoint, not to any one object, so the last-call stamp is
# shared. Two collectors in the same process must not each believe they have a fresh budget.
_LAST_CALL: dict[str, float] = {}


class _PacedGdelt:
    """Shared rate limiting. GDELT answers a breach with plain text and an HTTP 200."""

    def __init__(
        self,
        client: HttpClient | None = None,
        *,
        min_interval: float = MIN_INTERVAL_SECONDS,
        sleeper: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.client = client or HttpClient(
            timeout=DISCOVERY_TIMEOUT_SECONDS, retries=DISCOVERY_RETRIES
        )
        self.min_interval = min_interval
        self.sleeper = sleeper
        self.clock = clock

    def _pace(self) -> None:
        last = _LAST_CALL.get("doc")
        if last is not None:
            elapsed = self.clock() - last
            if elapsed < self.min_interval:
                self.sleeper(self.min_interval - elapsed)
        _LAST_CALL["doc"] = self.clock()

    def _payload(self, url: str, *, label: str) -> dict:
        response = self.client.get(url, accept="application/json")
        body = response.body.lstrip()
        if body.startswith(b"Please limit requests"):
            # GDELT signals throttling in plain text with a 200 status.
            raise HttpError(
                "rate_limited",
                "GDELT asked for a slower request rate; the request was skipped",
                status=response.status,
            )
        payload = response.json()
        if not isinstance(payload, dict):
            raise HttpError("invalid_json", f"unexpected GDELT response for {label}")
        return payload


class GdeltDiscovery(_PacedGdelt):
    """A discovery index, not a source of truth.

    Items returned here are candidate leads. They carry source_type `discovery_only` and
    can never be promoted to scored evidence on their own; they must be corroborated by a
    directly collected source first.
    """

    def collect(self, spec: DiscoveryQuery, *, window_hours: float) -> list[NewsItem]:
        self._pace()
        params = urlencode(
            {
                "query": spec.query,
                "mode": "artlist",
                "maxrecords": min(max(spec.max_records, 1), 250),
                "format": "json",
                "sort": "datedesc",
                "timespan": timespan_label(window_hours),
            }
        )
        payload = self._payload(f"{GDELT_DOC_URL}?{params}", label=spec.id)

        items: list[NewsItem] = []
        for article in payload.get("articles") or []:
            if not isinstance(article, dict):
                continue
            url = str(article.get("url") or "")
            if not url:
                continue
            domain = str(article.get("domain") or urlparse(url).netloc).casefold()
            items.append(
                NewsItem(
                    source_id=f"discovery:{spec.id}",
                    title=str(article.get("title") or "").strip(),
                    url=url,
                    published_at=_published(str(article.get("seendate") or "")),
                    publisher=domain,
                    domain=domain,
                    # Family is the domain: GDELT cannot tell us about editorial ownership,
                    # which is exactly why these cannot corroborate one another.
                    source_family=f"discovery:{domain}",
                    source_type="discovery_only",
                    discovery_route=f"GDELT discovery: {spec.title}",
                    language=str(article.get("language") or ""),
                )
            )
        return items


# ---------------------------------------------------------------------------
# Reporting volume over time.
#
# Counting how often a subject is reported and attesting that something happened are
# different operations. Everything below performs the first and never the second. A
# volume point is a measurement of coverage; it names no article, witnesses no event and
# cannot corroborate anything. The rule that a GDELT hit can never attest a claim is
# unchanged by its existence — `GdeltDiscovery` above remains the only path from this
# index into the corpus, and it still marks everything `discovery_only`.
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class VolumePoint:
    """One day of coverage volume: the share of monitored articles matching a query."""

    day: str
    value: float

    def to_dict(self) -> dict[str, float | str]:
        return {"day": self.day, "value": self.value}


def _volume_day(value: str) -> str:
    for fmt in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S", "%Y%m%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return ""


class GdeltVolumeTimeline(_PacedGdelt):
    """GDELT DOC 2.0 in `timelinevol` mode: how much a subject is being reported.

    The value is a percentage of all coverage GDELT monitored that day, so it is a proxy
    for tempo and nothing more. Levels are not comparable across queries and mean little
    on their own; only the direction of change against a stated baseline is usable.
    """

    def volume(self, query: str, *, start: date, end: date) -> list[VolumePoint]:
        self._pace()
        params = urlencode(
            {
                "query": query,
                "mode": "timelinevol",
                "format": "json",
                "startdatetime": start.strftime("%Y%m%d") + "000000",
                "enddatetime": end.strftime("%Y%m%d") + "235959",
            }
        )
        payload = self._payload(f"{GDELT_DOC_URL}?{params}", label="timelinevol")

        series = payload.get("timeline") or []
        if not series or not isinstance(series[0], dict):
            raise HttpError(
                "empty_timeline",
                f"GDELT returned no volume series for {start.isoformat()}..{end.isoformat()}",
            )
        points: list[VolumePoint] = []
        for row in series[0].get("data") or []:
            if not isinstance(row, dict):
                continue
            day = _volume_day(str(row.get("date") or ""))
            if not day:
                continue
            try:
                value = float(row.get("value"))
            except (TypeError, ValueError):
                continue
            points.append(VolumePoint(day=day, value=value))
        if not points:
            raise HttpError(
                "empty_timeline",
                f"GDELT returned an empty volume series for {start.isoformat()}..{end.isoformat()}",
            )
        points.sort(key=lambda p: p.day)
        return points
