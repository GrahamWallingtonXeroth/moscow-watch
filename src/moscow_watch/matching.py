from __future__ import annotations

import re
import unicodedata

_WORD_SPLIT = re.compile(r"[^0-9a-z]+")

# Standard denial and negation vocabulary. A headline that reports a denial of an event
# is not a report of the event, so these block a match unless a rule opts out.
DENIAL_TERMS = (
    "denies", "denied", "denial", "rejects", "rejected", "dismisses", "dismissed",
    "refutes", "refuted", "disputes", "disputed", "no plans", "not planning",
    "rules out", "ruled out", "declines", "declined", "false", "unfounded",
    "did not", "does not", "will not", "has not", "have not", "never",
    "no evidence", "denying",
)


def normalise(text: str) -> str:
    """Lowercase, strip accents, collapse punctuation, and pad so whole-word tests work."""
    decomposed = unicodedata.normalize("NFKD", str(text))
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return " " + " ".join(part for part in _WORD_SPLIT.split(stripped.casefold()) if part) + " "


def term_matches(haystack_normalised: str, term: str) -> bool:
    """Whole-word or whole-phrase containment. 'stop' must never match 'nonstop'."""
    needle = normalise(term).strip()
    if not needle:
        return False
    return f" {needle} " in haystack_normalised


def detect_negation(text: str, extra_terms: tuple[str, ...] = ()) -> list[str]:
    """Return the denial terms present, so a caller can explain why it refused a match."""
    haystack = normalise(text)
    return [term for term in DENIAL_TERMS + extra_terms if term_matches(haystack, term)]


def match_groups(
    text: str,
    required_groups: list[list[str]],
    excluded_any: list[str] | None = None,
    *,
    block_on_denial: bool = True,
) -> tuple[bool, list[str]]:
    """Every group must contribute at least one whole-word match.

    Returns (matched, matched_terms), the terms ordered and de-duplicated so the recorded
    classification basis is reproducible from the headline alone.
    """
    if not required_groups:
        return False, []
    haystack = normalise(text)
    for term in excluded_any or []:
        if term_matches(haystack, term):
            return False, []
    if block_on_denial and detect_negation(text):
        # "Moscow denies halting weapons to Iran" reports a denial, not a halt.
        return False, []
    matched: list[str] = []
    for group in required_groups:
        hits = [term for term in group if term_matches(haystack, term)]
        if not hits:
            return False, []
        for hit in hits:
            if hit not in matched:
                matched.append(hit)
    return True, matched
