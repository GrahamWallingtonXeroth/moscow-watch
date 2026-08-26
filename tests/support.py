from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError

from moscow_watch.http import HttpResponse
from moscow_watch.models import utc_now_iso

FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def fixture_json(name: str):
    return json.loads(fixture(name))


class FakeClient:
    """Deterministic stand-in for HttpClient. Records every URL requested.

    Applies the same content-type check the real client does, so a fake can never pass a
    check the real client would fail.
    """

    def __init__(self, *, payload=None, text="", content_type="application/xml", routes=None):
        self.payload = payload
        self.text_body = text
        self.content_type = content_type
        self.routes = routes or {}
        self.calls: list[str] = []

    def _route(self, url: str):
        for key, value in self.routes.items():
            if key in url:
                return value
        return None

    def get(self, url: str, *, accept: str = "*/*") -> HttpResponse:
        self.calls.append(url)
        routed = self._route(url)
        if routed is not None:
            body = routed
        elif self.text_body:
            body = self.text_body
        else:
            body = self.payload
        if body is None:
            body = b""
        if not isinstance(body, (bytes, str)):
            body = json.dumps(body)
        if isinstance(body, str):
            body = body.encode("utf-8")
        return HttpResponse(
            url=url,
            status=200,
            headers={"content-type": self.content_type},
            body=body,
            fetched_at=utc_now_iso(),
        )

    def get_json(self, url: str):
        self.calls.append(url)
        routed = self._route(url)
        return routed if routed is not None else self.payload

    def get_xml_text(self, url: str) -> str:
        return (
            self.get(url)
            .require_content_type(
                "xml", "rss+xml", "atom+xml", "text/xml", "application/xml", "rdf+xml", "text/plain"
            )
            .text()
        )


class CountingSleeper:
    """Captures backoff without spending real time."""

    def __init__(self) -> None:
        self.delays: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.delays.append(seconds)


class _Headers(dict):
    def get(self, key, default=None):
        for existing, value in self.items():
            if existing.casefold() == key.casefold():
                return value
        return default


class _FakeResponse:
    def __init__(self, body: bytes, headers: dict):
        self.body = body
        self.headers = _Headers(headers)
        self.status = 200

    def read(self) -> bytes:
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FakeHTTPErrorOpener:
    """Raises a scripted sequence of HTTPError/success for HttpClient tests."""

    def __init__(self, statuses: list[int], *, headers=None, body=b"{}"):
        self.statuses = list(statuses)
        self.headers = headers or {}
        self.body = body
        self.attempts = 0

    def __call__(self, request, timeout=None):
        self.attempts += 1
        status = self.statuses.pop(0) if self.statuses else 200
        if status >= 400:
            raise HTTPError(
                request.full_url, status, f"error {status}", _Headers(self.headers), None
            )
        return _FakeResponse(self.body, self.headers)


class MemoryStore:
    """In-memory JsonlStore stand-in. Tests never touch the filesystem or the network."""

    def __init__(self, tables: dict[str, list[dict]] | None = None) -> None:
        self.tables = {k: list(v) for k, v in (tables or {}).items()}

    def read(self, name: str) -> list[dict]:
        return list(self.tables.get(name, []))

    def append_unique(self, name: str, records, key: str = "id") -> int:
        existing = {r.get(key) for r in self.tables.get(name, [])}
        fresh = [r for r in records if r.get(key) not in existing]
        self.tables.setdefault(name, []).extend(fresh)
        return len(fresh)
