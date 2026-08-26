"""Russia–Iran senior diplomatic contact counter.

This is the highest-value indicator in the project, because it is the only thing that
separates H3 (Russia pulls back from Tehran) from H4 (Russia leans in, at American
request). Both hypotheses predict the same *Iran* outcomes — a pause, resumed talks, a
softer nuclear posture — and commentary will read either as "Russia helped". What tells
them apart is simply which direction Russian officials are travelling.

Two honesty constraints are built in rather than documented and forgotten:

1. This counts **reported** contacts. Unreported diplomacy is exactly what this story is
   about, so the count is a floor, never a total. The label says so everywhere it appears.
2. Every counted contact stores the URL it came from, so the number is auditable rather
   than asserted. A reader can check any fortnight's count by following the links.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from typing import Any

from ..matching import match_groups, normalise, term_matches
from ..models import stable_id

# A contact needs a Russian actor, an Iranian actor, and a word implying they engaged.
RUSSIA_TERMS = (
    "russia", "russian", "moscow", "kremlin", "lavrov", "putin", "ryabkov", "shoigu",
    "peskov", "rosatom", "likhachev",
)
IRAN_TERMS = (
    "iran", "iranian", "tehran", "araghchi", "khamenei", "pezeshkian", "larijani",
)
CONTACT_TERMS = (
    "talks", "meeting", "met", "meets", "visit", "visited", "visits", "call", "phone call",
    "summit", "delegation", "consultations", "discussed", "discussions", "signed",
    "agreement", "envoy", "ambassador", "readout", "spoke",
)

# Contacts at this level are the ones that carry signal; a consular note is not a policy act.
SENIOR_TERMS = (
    "president", "foreign minister", "minister", "deputy foreign minister", "envoy",
    "spokesman", "spokesperson", "chief", "director", "ambassador", "secretary",
    "lavrov", "putin", "ryabkov", "araghchi", "pezeshkian", "larijani", "likhachev",
)

REQUIRED_GROUPS = [list(RUSSIA_TERMS), list(IRAN_TERMS), list(CONTACT_TERMS)]


@dataclass(slots=True)
class Contact:
    """One reported Russia–Iran contact, with the source that reported it."""

    observed_on: str
    title: str
    url: str
    publisher: str
    source_family: str
    source_type: str
    matched_terms: list[str] = field(default_factory=list)
    senior: bool = False
    source: str = "contact_counter"

    @property
    def id(self) -> str:
        # Keyed on URL so re-collection never double-counts a contact.
        return stable_id("contact", self.url or self.title)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, **asdict(self)}


def _is_senior(text: str) -> bool:
    haystack = normalise(text)
    return any(term_matches(haystack, term) for term in SENIOR_TERMS)


def extract_contacts(items: Iterable[dict[str, Any]]) -> list[Contact]:
    """Find reported contacts in an already-collected corpus.

    Runs over the same items the feed collectors stored, so it costs no extra request and
    every hit keeps its original provenance.
    """
    found: dict[str, Contact] = {}
    for item in items:
        text = f"{item.get('title', '')} {item.get('summary', '')}"
        matched, terms = match_groups(text, REQUIRED_GROUPS)
        if not matched:
            continue
        url = str(item.get("url") or "")
        published = str(item.get("published_at") or "")[:10]
        if not published:
            continue
        contact = Contact(
            observed_on=published,
            title=str(item.get("title") or ""),
            url=url,
            publisher=str(item.get("publisher") or ""),
            source_family=str(item.get("source_family") or ""),
            source_type=str(item.get("source_type") or ""),
            matched_terms=terms,
            senior=_is_senior(text),
        )
        found.setdefault(contact.id, contact)
    return sorted(found.values(), key=lambda c: c.observed_on)


def fortnight_start(day: date, *, anchor: date) -> date:
    """Bucket a date into fortnights measured from a fixed anchor."""
    delta = (day - anchor).days
    return anchor + timedelta(days=(delta // 14) * 14)


def fortnightly_series(
    contacts: Iterable[dict[str, Any]],
    *,
    anchor: date,
    senior_only: bool = False,
) -> list[dict[str, Any]]:
    """Counts per fortnight, with the citing URLs kept alongside each bucket."""
    buckets: dict[date, list[dict[str, Any]]] = {}
    for row in contacts:
        if senior_only and not row.get("senior"):
            continue
        try:
            day = date.fromisoformat(str(row.get("observed_on"))[:10])
        except (TypeError, ValueError):
            continue
        buckets.setdefault(fortnight_start(day, anchor=anchor), []).append(row)

    series: list[dict[str, Any]] = []
    for start in sorted(buckets):
        rows = buckets[start]
        series.append(
            {
                "fortnight_start": start.isoformat(),
                "fortnight_end": (start + timedelta(days=13)).isoformat(),
                "count": len(rows),
                "senior_count": sum(1 for r in rows if r.get("senior")),
                "citations": [
                    {"title": r.get("title", ""), "url": r.get("url", ""),
                     "publisher": r.get("publisher", "")}
                    for r in rows
                ],
            }
        )
    return series


def baseline(
    series: list[dict[str, Any]], *, before: date
) -> dict[str, Any]:
    """Pre-event baseline, so 'up' or 'down' is measured against something stated."""
    prior = [b for b in series if date.fromisoformat(b["fortnight_start"]) < before]
    if not prior:
        return {"fortnights": 0, "mean_per_fortnight": None, "before": before.isoformat()}
    counts = [b["count"] for b in prior]
    return {
        "fortnights": len(prior),
        "mean_per_fortnight": round(sum(counts) / len(counts), 2),
        "max_per_fortnight": max(counts),
        "before": before.isoformat(),
    }


def direction(
    series: list[dict[str, Any]], base: dict[str, Any], *, tolerance: float = 0.5
) -> str:
    """down / flat / up against the stated baseline, or 'insufficient data'.

    Deliberately coarse. This feeds one axis of the discriminator map, and a finer reading
    than the data supports would be false precision.
    """
    mean = base.get("mean_per_fortnight")
    if mean is None or not series:
        return "insufficient data"
    latest = series[-1]["count"]
    if latest > mean + tolerance:
        return "up"
    if latest < mean - tolerance:
        return "down"
    return "flat"
