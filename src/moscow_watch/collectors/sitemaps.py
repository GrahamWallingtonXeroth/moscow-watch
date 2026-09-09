"""Link-only monitoring for analytical publishers with no permitted RSS feed.

This collector deliberately reads sitemap metadata and nothing else. It does not fetch an
article body, map, dataset or endnote, and its records never enter corroboration counting.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import UTC, date, datetime, timedelta
from urllib.parse import urlparse

from ..config import AnalysisSource
from ..http import HttpClient, HttpError
from ..models import AnalysisReference, parse_time
from .feeds import canonical_url, domain_of, parse_date

MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}
DATED_SLUG = re.compile(
    r"-(?P<month>" + "|".join(MONTHS) + r")-(?P<day>\d{1,2})-(?P<year>\d{4})/?$",
    re.IGNORECASE,
)


def _local_name(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element.iter() if _local_name(child) == name]


def _root(xml_text: str, source: AnalysisSource, expected: str) -> ET.Element:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise HttpError(
            "invalid_xml", f"{source.title} sitemap did not parse as XML: {exc}"
        ) from exc
    if _local_name(root) != expected:
        raise HttpError(
            "invalid_sitemap", f"{source.title} returned {_local_name(root)!r}, not {expected!r}"
        )
    return root


def assessment_metadata(url: str) -> tuple[str, date] | None:
    """Derive the dated product title from its stable URL; no page text is copied."""
    match = DATED_SLUG.search(urlparse(url).path)
    if not match:
        return None
    month_name = match.group("month").casefold()
    try:
        assessment_date = date(
            int(match.group("year")), MONTHS[month_name], int(match.group("day"))
        )
    except ValueError:
        return None
    title = (
        "Russian Offensive Campaign Assessment, "
        f"{month_name.title()} {assessment_date.day}, {assessment_date.year}"
    )
    return title, assessment_date


def recent_post_sitemaps(
    source: AnalysisSource,
    xml_text: str,
    *,
    window_hours: float,
    now: datetime,
) -> list[str]:
    """Select changed post shards, with a bounded latest-shard fallback.

    A quiet publisher is still a healthy source. If no shard changed inside the
    collection window, the two newest post shards are checked and may legitimately
    yield no references. This keeps "no new assessment" distinct from source failure.
    """
    root = _root(xml_text, source, "sitemapindex")
    cutoff = now.astimezone(UTC) - timedelta(hours=window_hours)
    source_host = domain_of(source.url)
    candidates: list[tuple[datetime, str]] = []
    for item in _children(root, "sitemap"):
        loc = _children(item, "loc")
        modified_node = _children(item, "lastmod")
        if not loc or not modified_node:
            continue
        url = canonical_url((loc[0].text or "").strip())
        filename = urlparse(url).path.rsplit("/", 1)[-1]
        modified = parse_date(modified_node[0].text or "")
        if (
            not url
            or domain_of(url) != source_host
            or not filename.startswith("post-sitemap")
            or not modified
        ):
            continue
        try:
            changed_at = parse_time(modified)
        except (TypeError, ValueError):
            continue
        candidates.append((changed_at, url))
    candidates.sort(reverse=True)
    recent = [candidate for candidate in candidates if candidate[0] >= cutoff]
    # Always include the two newest post shards. That catches a sitemap rollover on a
    # first run without turning the entire publisher index into a crawl.
    selected = sorted(set([*recent, *candidates[:2]]), reverse=True)
    # The cap is a defence against a malformed upstream index causing an unbounded crawl.
    return [url for _, url in selected[:8]]


def assessment_references(
    source: AnalysisSource,
    xml_text: str,
    *,
    window_hours: float,
    now: datetime,
    collected_at: str,
) -> list[AnalysisReference]:
    root = _root(xml_text, source, "urlset")
    cutoff = now.astimezone(UTC) - timedelta(hours=window_hours)
    cutoff_date = cutoff.date()
    today = now.astimezone(UTC).date()
    source_host = domain_of(source.url)
    results: list[AnalysisReference] = []
    for item in _children(root, "url"):
        loc = _children(item, "loc")
        modified_node = _children(item, "lastmod")
        if not loc or not modified_node:
            continue
        url = canonical_url((loc[0].text or "").strip())
        modified = parse_date(modified_node[0].text or "")
        if (
            not url
            or domain_of(url) != source_host
            or not urlparse(url).path.startswith(source.path_prefix)
            or not modified
        ):
            continue
        metadata = assessment_metadata(url)
        if not metadata:
            continue
        title, assessment_date = metadata
        try:
            modified_at = parse_time(modified)
        except (TypeError, ValueError):
            continue
        # Include either a recent assessment or an older assessment that the publisher
        # freshly marked as modified. The two dates remain separate in the record.
        if assessment_date > today or (
            assessment_date < cutoff_date and modified_at < cutoff
        ):
            continue
        results.append(
            AnalysisReference(
                source_id=source.id,
                title=title,
                url=url,
                publisher=source.publisher,
                source_family=source.source_family,
                assessment_date=assessment_date.isoformat(),
                sitemap_modified_at=modified,
                attribution=f"Source: {source.publisher}",
                rights_url=source.rights_url,
                collected_at=collected_at,
            )
        )
    return results


class SitemapAnalysisCollector:
    """Collects bounded bibliographic metadata from a publisher-advertised sitemap."""

    def __init__(self, client: HttpClient | None = None) -> None:
        self.client = client or HttpClient()
        self.warnings: list[str] = []

    def collect(
        self,
        source: AnalysisSource,
        *,
        window_hours: float,
        now: datetime | None = None,
        collected_at: str = "",
    ) -> list[AnalysisReference]:
        self.warnings = []
        observed_at = now or datetime.now(UTC)
        captured_at = collected_at or observed_at.replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        )
        index = self.client.get_xml_text(source.url)
        shards = recent_post_sitemaps(
            source, index, window_hours=window_hours, now=observed_at
        )
        if not shards:
            raise HttpError(
                "empty_sitemap", f"{source.title} had no post sitemap in its sitemap index"
            )
        found: dict[str, AnalysisReference] = {}
        parsed_shards = 0
        for shard in shards:
            try:
                references = assessment_references(
                    source,
                    self.client.get_xml_text(shard),
                    window_hours=window_hours,
                    now=observed_at,
                    collected_at=captured_at,
                )
            except Exception as exc:
                detail = exc.summary if isinstance(exc, HttpError) else str(exc)
                self.warnings.append(f"{urlparse(shard).path}: {detail}")
                continue
            parsed_shards += 1
            for reference in references:
                found.setdefault(reference.id, reference)
        if parsed_shards == 0:
            detail = "; ".join(self.warnings) or "no readable post sitemap"
            raise HttpError(
                "sitemap_shards_failed",
                f"{source.title} could not read any selected post sitemap: {detail}",
            )
        return sorted(
            found.values(), key=lambda item: item.sitemap_modified_at, reverse=True
        )[: source.max_items]
