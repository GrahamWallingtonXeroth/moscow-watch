from __future__ import annotations

import gzip
import json
import time
import zlib
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import utc_now_iso

USER_AGENT = (
    "moscow-watch/0.1 "
    "(+https://github.com/GrahamWallingtonXeroth/moscow-watch)"
)

# Permanent failures. Retrying these wastes the workflow budget and tells us nothing new.
PERMANENT_STATUSES = {400, 401, 403, 404, 405, 410, 451}


def short_url(url: str) -> str:
    """Host and path only. A 400-character query string buries the actual error."""
    from urllib.parse import urlparse

    parts = urlparse(url)
    if not parts.netloc:
        return url[:120]
    return f"{parts.netloc}{parts.path}"


class HttpError(RuntimeError):
    """A source failure carrying a stable category, so repeated failures stay identical."""

    def __init__(self, category: str, message: str, *, status: int | None = None) -> None:
        super().__init__(message)
        self.category = category
        self.status = status

    @property
    def summary(self) -> str:
        return f"{self.category}: {self}"


GZIP_MAGIC = b"\x1f\x8b"


def decode_body(body: bytes, content_encoding: str = "") -> bytes:
    """Transparently decompress.

    Some feeds (UN News among them) return gzip regardless of Accept-Encoding, and a raw
    gzip stream handed to an XML parser fails as "not well-formed at line 1, column 0",
    which reads like a broken feed rather than a compressed one.
    """
    encoding = content_encoding.casefold().strip()
    try:
        if encoding == "gzip" or body[:2] == GZIP_MAGIC:
            return gzip.decompress(body)
        if encoding == "deflate":
            return zlib.decompress(body, -zlib.MAX_WBITS)
    except (OSError, zlib.error, EOFError):
        return body
    return body


@dataclass(slots=True)
class HttpResponse:
    url: str
    status: int
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    fetched_at: str = ""

    @property
    def content_type(self) -> str:
        return self.headers.get("content-type", "").split(";")[0].strip().casefold()

    def text(self, encoding: str = "utf-8") -> str:
        return self.body.decode(encoding, errors="replace")

    def json(self) -> Any:
        try:
            return json.loads(self.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise HttpError(
                "invalid_json",
                f"{short_url(self.url)} returned {self.content_type or 'unknown content'} "
                f"that is not valid JSON: {self.body[:120]!r}",
                status=self.status,
            ) from exc

    def require_content_type(self, *allowed: str) -> HttpResponse:
        """Reject an HTML error page served in place of XML or JSON."""
        actual = self.content_type
        if actual and not any(actual == item or actual.endswith(item) for item in allowed):
            raise HttpError(
                "wrong_content_type",
                f"{short_url(self.url)} returned content-type {actual!r}, expected one of "
                f"{', '.join(allowed)}. First bytes: {self.body[:120]!r}",
                status=self.status,
            )
        return self


def _retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        pass
    try:
        target = parsedate_to_datetime(value)
    except (TypeError, ValueError, OverflowError):
        return None
    from datetime import datetime

    delta = (target - datetime.now(UTC)).total_seconds()
    return max(delta, 0.0)


class HttpClient:
    """A small, honest HTTP client with bounded retries and inspectable responses."""

    def __init__(
        self,
        *,
        timeout: float = 15.0,
        retries: int = 2,
        user_agent: str = USER_AGENT,
        max_backoff: float = 8.0,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        self.timeout = timeout
        self.retries = retries
        self.user_agent = user_agent
        self.max_backoff = max_backoff
        self.sleeper = sleeper

    def get(self, url: str, *, accept: str = "*/*") -> HttpResponse:
        request = Request(url, headers={"Accept": accept, "User-Agent": self.user_agent})
        last: HttpError | None = None
        for attempt in range(self.retries + 1):
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    headers = {
                        key.casefold(): value for key, value in response.headers.items()
                    }
                    return HttpResponse(
                        url=url,
                        status=getattr(response, "status", 200) or 200,
                        headers=headers,
                        body=decode_body(
                            response.read(), headers.get("content-encoding", "")
                        ),
                        fetched_at=utc_now_iso(),
                    )
            except HTTPError as exc:
                status = int(exc.code)
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                exc.close()
                if status in PERMANENT_STATUSES:
                    # Fail immediately. A 404 will still be a 404 in two seconds.
                    raise HttpError(
                        f"http_{status}", f"{short_url(url)} returned HTTP {status}", status=status
                    ) from exc
                last = HttpError(
                    f"http_{status}", f"{short_url(url)} returned HTTP {status}", status=status
                )
                delay = _retry_after_seconds(retry_after) if status == 429 else None
                self._wait(attempt, delay)
            except (URLError, TimeoutError, OSError) as exc:
                last = HttpError("network", f"{short_url(url)} could not be reached: {exc}")
                self._wait(attempt, None)
        raise last or HttpError("network", f"{short_url(url)} failed for an unknown reason")

    def _wait(self, attempt: int, explicit: float | None) -> None:
        if attempt >= self.retries:
            return
        delay = explicit if explicit is not None else min(0.5 * (2**attempt), self.max_backoff)
        self.sleeper(min(delay, self.max_backoff))

    def get_json(self, url: str) -> Any:
        return self.get(url, accept="application/json").json()

    def get_xml_text(self, url: str) -> str:
        response = self.get(
            url, accept="application/rss+xml, application/atom+xml, application/xml, text/xml"
        ).require_content_type(
            "xml", "rss+xml", "atom+xml", "text/xml", "application/xml", "rdf+xml", "text/plain"
        )
        return response.text()
