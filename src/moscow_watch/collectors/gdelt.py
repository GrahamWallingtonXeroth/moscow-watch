from __future__ import annotations

import time
from collections.abc import Callable
from datetime import UTC, datetime
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


class GdeltDiscovery:
    """A discovery index, not a source of truth.

    Items returned here are candidate leads. They carry source_type `discovery_only` and
    can never be promoted to scored evidence on their own; they must be corroborated by a
    directly collected source first.
    """

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
        self._last_call: float | None = None

    def _pace(self) -> None:
        if self._last_call is None:
            self._last_call = self.clock()
            return
        elapsed = self.clock() - self._last_call
        if elapsed < self.min_interval:
            self.sleeper(self.min_interval - elapsed)
        self._last_call = self.clock()

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
        response = self.client.get(f"{GDELT_DOC_URL}?{params}", accept="application/json")
        body = response.body.lstrip()
        if body.startswith(b"Please limit requests"):
            # GDELT signals throttling in plain text with a 200 status.
            raise HttpError(
                "rate_limited",
                "GDELT asked for a slower request rate; discovery skipped this run",
                status=response.status,
            )
        payload = response.json()
        if not isinstance(payload, dict):
            raise HttpError("invalid_json", f"unexpected GDELT response for {spec.id}")

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
