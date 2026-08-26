from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse, urlunparse

from ..config import NewsSource
from ..http import HttpClient, HttpError
from ..models import NewsItem, within_window

TAG_RE = re.compile(r"<[^>]+>")
TRACKING_PREFIXES = ("utm_", "cmpid", "cmp", "ito", "ns_", "at_", "fbclid", "gclid")


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext()).strip()


def _first(item: ET.Element, *paths: str) -> str:
    for path in paths:
        value = _text(item.find(path))
        if value:
            return value
    return ""


def clean(value: str) -> str:
    return html.unescape(TAG_RE.sub(" ", html.unescape(value))).strip()


def parse_date(value: str) -> str:
    if not value:
        return ""
    raw = value.strip()
    try:
        return (
            parsedate_to_datetime(raw)
            .astimezone(UTC)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
    except (TypeError, ValueError, OverflowError):
        pass
    try:
        return (
            datetime.fromisoformat(raw.replace("Z", "+00:00"))
            .astimezone(UTC)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z")
        )
    except (TypeError, ValueError):
        return ""


def canonical_url(url: str) -> str:
    """Strip tracking parameters and fragments so the same article has one identity."""
    if not url:
        return ""
    parts = urlparse(url.strip())
    if not parts.scheme or not parts.netloc:
        return url.strip()
    kept = [
        pair
        for pair in parts.query.split("&")
        if pair and not pair.split("=")[0].casefold().startswith(TRACKING_PREFIXES)
    ]
    return urlunparse(
        (parts.scheme, parts.netloc.casefold(), parts.path.rstrip("/") or "/", "", "&".join(kept), "")
    )


def domain_of(url: str) -> str:
    return urlparse(url).netloc.casefold().removeprefix("www.")


def publisher_matches(domain: str, expected: str) -> bool:
    """Accept the publisher's own domain and its subdomains, and nothing that merely contains it."""
    normalised = domain.casefold().strip().removeprefix("www.")
    expected = expected.casefold().strip().removeprefix("www.")
    return normalised == expected or normalised.endswith("." + expected)


def parse_feed(spec: NewsSource, xml_text: str) -> list[NewsItem]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise HttpError(
            "invalid_xml", f"{spec.title} feed did not parse as XML: {exc}"
        ) from exc
    items = root.findall(".//item") or root.findall(".//{*}entry")
    if not items:
        raise HttpError(
            "empty_feed", f"{spec.title} feed contained no <item> or <entry> elements"
        )

    results: list[NewsItem] = []
    for item in items:
        title = clean(_first(item, "title", "{*}title"))
        link = _first(item, "link", "{*}link[@rel='alternate']")
        if not link:
            element = item.find("{*}link")
            if element is not None:
                link = element.attrib.get("href", "")
        link = canonical_url(link)
        if not title or not link:
            continue
        published = parse_date(
            _first(item, "pubDate", "published", "{*}published", "{*}updated", "{*}date")
        )
        summary = clean(
            _first(item, "description", "summary", "{*}summary", "{*}content")
        )
        results.append(
            NewsItem(
                source_id=spec.id,
                title=title,
                url=link,
                published_at=published,
                publisher=spec.publisher,
                source_family=spec.source_family,
                source_type=spec.source_type,
                standpoint=spec.standpoint,
                domain=domain_of(link),
                # Feed-provided summary only, truncated. Article bodies are never fetched.
                summary=summary[:400],
                discovery_route=f"{spec.title} feed",
            )
        )
    return results


class NewsFeedCollector:
    """Fetches each configured source exactly once per run.

    Every directional rule is then applied locally to that single corpus, so adding a
    thirteenth evidence rule costs zero extra upstream requests.
    """

    def __init__(self, client: HttpClient | None = None) -> None:
        self.client = client or HttpClient()

    def collect(
        self,
        spec: NewsSource,
        *,
        window_hours: float,
        now: datetime | None = None,
    ) -> list[NewsItem]:
        xml_text = self.client.get_xml_text(spec.url)
        items = parse_feed(spec, xml_text)
        kept: dict[str, NewsItem] = {}
        for item in items:
            if item.published_at and not within_window(item.published_at, window_hours, now=now):
                continue
            if spec.include_any:
                haystack = f"{item.title} {item.summary}".casefold()
                if not any(term.casefold() in haystack for term in spec.include_any):
                    continue
            # Keyed on canonical URL, so the same article is never collected twice.
            kept.setdefault(item.url, item)
        return list(kept.values())
