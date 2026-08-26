from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .config import ClaimRule, Config
from .dedupe import group_duplicates
from .matching import match_groups
from .models import parse_time, stable_id, utc_now_iso

# The label IS the output. Nothing numeric is attached to a claim and nothing is summed:
# the repo publishes what was found and how well it is attested, and a human decides what
# it means in the article.
STATUSES = (
    "primary_documented",
    "corroborated",
    "single_source",
    "contested",
    "discovery_only",
)

STATUS_EXPLANATION = {
    "primary_documented": "An official record documents this action directly.",
    "corroborated": "Reported by at least two editorially independent newsrooms.",
    "single_source": "Reported by one source family only. Shown as a lead; contributes nothing.",
    "contested": "Independent sources conflict on this claim. Contributes nothing until resolved.",
    "discovery_only": "Surfaced by the discovery index alone; no directly collected source carried it.",
}


@dataclass(slots=True)
class Citation:
    url: str
    title: str
    publisher: str
    source_family: str
    source_type: str
    published_at: str
    discovery_route: str = ""
    standpoint: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class Claim:
    """One promoted assertion, with everything a reader needs to check it."""

    signal_id: str
    hypothesis_id: str
    verdict: str
    claim_type: str
    title: str
    corroboration_status: str
    matched_terms: list[str] = field(default_factory=list)
    source_families: list[str] = field(default_factory=list)
    discovery_families: list[str] = field(default_factory=list)
    citations: list[dict[str, Any]] = field(default_factory=list)
    basis: str = ""
    first_seen_at: str = ""
    note: str = ""
    promoted_at: str = field(default_factory=utc_now_iso)

    @property
    def id(self) -> str:
        # Stable across runs: same rule, same hypothesis, same story cluster.
        anchor = min((c.get("url", "") for c in self.citations), default=self.title)
        return stable_id("claim", self.signal_id, self.hypothesis_id, anchor)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, **asdict(self)}


def _text_of(item: dict[str, Any]) -> str:
    return f"{item.get('title', '')} {item.get('summary', '')}"


def _within(a: str, b: str, hours: float) -> bool:
    """Two reports corroborate only if they land inside the configured window."""
    if not a or not b:
        return True
    try:
        delta = abs((parse_time(a) - parse_time(b)).total_seconds()) / 3600.0
    except (TypeError, ValueError):
        return True
    return delta <= hours


def _status_for(
    signal: ClaimRule,
    qualifying_families: set[str],
    source_types: set[str],
    has_conflict: bool,
) -> tuple[str, str]:
    """`qualifying_families` excludes discovery families by construction.

    A discovery hit is a pointer to a story, not an independent witness to it, so it can
    never be the second source that promotes a claim.
    """
    if has_conflict:
        return "contested", "Independent sources conflict on this claim."

    directly_collected = source_types & {"primary_record", "independent_reporting"}
    if not directly_collected:
        return "discovery_only", "Discovery index only; no directly collected source carried this."

    if signal.claim_type == "official_action":
        # Only a primary record can establish that an institution actually did something.
        if "primary_record" in source_types:
            return "primary_documented", ""
        if len(qualifying_families) >= 2:
            return "corroborated", "No primary record found; two independent newsrooms report it."
        return (
            "single_source",
            "An official action needs a primary record or two independent newsrooms.",
        )

    if signal.claim_type == "actor_statement":
        # Self-establishing: the actor saying it is the fact being recorded.
        if "primary_record" in source_types:
            return "primary_documented", ""
        return (
            "corroborated" if len(qualifying_families) >= 2 else "single_source",
            "Establishes only that the actor said this.",
        )

    # external_observable and allegation both need independent agreement.
    if len(qualifying_families) >= 2:
        return "corroborated", ""
    return "single_source", ""


def promote_claims(
    config: Config,
    items: list[dict[str, Any]],
    *,
    conflicts_by_story: dict[str, bool] | None = None,
) -> list[dict[str, Any]]:
    """Match every rule locally, cluster syndicated copies, then apply promotion rules.

    A claim is scored once regardless of how many outlets repeated it, and only if the
    evidence behind it clears the bar its claim_type demands.
    """
    claims: list[dict[str, Any]] = []
    by_signal_hypothesis: dict[tuple[str, str], list[dict[str, Any]]] = {}

    for signal in config.claim_rules:
        matches: list[tuple[dict[str, Any], list[str]]] = []
        for item in items:
            matched, terms = match_groups(
                _text_of(item), signal.required_groups, signal.excluded_any
            )
            if matched:
                matches.append((item, terms))
        if not matches:
            continue
        by_signal_hypothesis[(signal.id, signal.hypothesis_id)] = [m[0] for m in matches]

        # One story, however many outlets carried it.
        for group in group_duplicates([m[0] for m in matches]):
            terms_for = {
                str(item.get("id")): terms for item, terms in matches
            }
            families: set[str] = set()
            qualifying_families: set[str] = set()
            source_types: set[str] = set()
            citations: list[dict[str, Any]] = []
            seen_families: set[str] = set()
            anchor_time = ""
            all_terms: list[str] = []

            for item in sorted(group, key=lambda i: str(i.get("published_at", ""))):
                family = str(item.get("source_family") or item.get("domain") or "unknown")
                source_type = str(item.get("source_type") or "discovery_only")
                published = str(item.get("published_at", ""))
                if not anchor_time:
                    anchor_time = published
                # Corroboration must happen inside the rule's window.
                if family not in seen_families and not _within(
                    anchor_time, published, signal.corroboration_window_hours
                ):
                    continue
                families.add(family)
                source_types.add(source_type)
                seen_families.add(family)
                if source_type in {"primary_record", "independent_reporting"}:
                    qualifying_families.add(family)
                for term in terms_for.get(str(item.get("id")), []):
                    if term not in all_terms:
                        all_terms.append(term)
                citations.append(
                    Citation(
                        url=str(item.get("url", "")),
                        title=str(item.get("title", "")),
                        publisher=str(item.get("publisher", "")),
                        source_family=family,
                        source_type=source_type,
                        published_at=published,
                        discovery_route=str(item.get("discovery_route", "")),
                        standpoint=str(item.get("standpoint", "")),
                    ).to_dict()
                )

            if not citations:
                continue
            story_key = citations[0]["url"]
            has_conflict = bool((conflicts_by_story or {}).get(story_key))
            status, note = _status_for(
                signal, qualifying_families, source_types, has_conflict
            )
            claims.append(
                Claim(
                    signal_id=signal.id,
                    hypothesis_id=signal.hypothesis_id,
                    verdict=signal.verdict,
                    claim_type=signal.claim_type,
                    title=citations[0]["title"],
                    corroboration_status=status,
                    matched_terms=all_terms,
                    source_families=sorted(qualifying_families),
                    discovery_families=sorted(families - qualifying_families),
                    citations=citations,
                    basis=signal.basis,
                    first_seen_at=anchor_time,
                    note=note or STATUS_EXPLANATION.get(status, ""),
                ).to_dict()
            )

    return _resolve_conflicts(claims)


def _resolve_conflicts(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One story cannot both support and refute the same hypothesis."""
    by_story: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for claim in claims:
        anchor = claim["citations"][0]["url"] if claim["citations"] else claim["title"]
        by_story.setdefault((anchor, claim["hypothesis_id"]), []).append(claim)

    resolved: list[dict[str, Any]] = []
    for group in by_story.values():
        verdicts = {c["verdict"] for c in group}
        if len(verdicts) > 1:
            exemplar = group[0]
            resolved.append(
                {
                    **exemplar,
                    "verdict": "contested",
                    "corroboration_status": "contested",
                    "conflicting_rules": sorted({c["signal_id"] for c in group}),
                    "note": (
                        "Opposing pre-registered rules matched this story. It is shown for "
                        "transparency and contributes nothing to any score."
                    ),
                }
            )
            continue
        # One story, one claim per hypothesis, however many rules it tripped.
        resolved.append(group[0])
    resolved.sort(
        key=lambda c: (c["corroboration_status"] != "corroborated", str(c["first_seen_at"])),
        reverse=False,
    )
    return resolved


def attested(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Claims that met their evidentiary bar. Still not a verdict about any hypothesis."""
    return [
        c
        for c in claims
        if c.get("corroboration_status") in {"primary_documented", "corroborated"}
    ]


def leads(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Everything else: shown so a reader can see what was found and why it fell short."""
    return [
        c
        for c in claims
        if c.get("corroboration_status") in {"single_source", "discovery_only", "contested"}
    ]
