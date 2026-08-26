from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .matching import normalise

SHINGLE_SIZE = 4
NEAR_DUPLICATE_THRESHOLD = 0.6

# Words that carry no distinguishing signal in a headline.
STOPWORDS = frozenset(
    """a an and are as at be by for from has have in is it its of on or that the to was were
    with says say said after over new amid what we know live updates""".split()
)


def title_tokens(title: str) -> list[str]:
    return [word for word in normalise(title).split() if word not in STOPWORDS]


def shingles(title: str, size: int = SHINGLE_SIZE) -> set[str]:
    tokens = title_tokens(title)
    if len(tokens) < size:
        return {" ".join(tokens)} if tokens else set()
    return {" ".join(tokens[i : i + size]) for i in range(len(tokens) - size + 1)}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    intersection = len(left & right)
    union = len(left | right)
    return intersection / union if union else 0.0


def is_near_duplicate(
    first: str, second: str, *, threshold: float = NEAR_DUPLICATE_THRESHOLD
) -> bool:
    """Deterministic near-duplicate test for syndicated copies of one story."""
    first_normalised = " ".join(title_tokens(first))
    second_normalised = " ".join(title_tokens(second))
    if not first_normalised or not second_normalised:
        return False
    if first_normalised == second_normalised:
        return True
    return jaccard(shingles(first), shingles(second)) >= threshold


def group_duplicates(items: Iterable[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Cluster articles that are the same story.

    Same canonical URL, or a near-identical normalised headline, means one story however
    many outlets carried it.
    """
    groups: list[list[dict[str, Any]]] = []
    by_url: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        url = str(item.get("url") or "")
        if url and url in by_url:
            by_url[url].append(item)
            continue
        title = str(item.get("title") or "")
        placed = False
        for group in groups:
            if is_near_duplicate(str(group[0].get("title") or ""), title):
                group.append(item)
                placed = True
                break
        if not placed:
            group = [item]
            groups.append(group)
        else:
            group = next(g for g in groups if item in g)
        if url:
            by_url[url] = group
    return groups
