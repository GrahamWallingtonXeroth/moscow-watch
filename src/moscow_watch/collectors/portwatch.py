"""IMF PortWatch daily chokepoint transits.

This is the project's one counted physical quantity: ships, not statements. Everything
else in the repo is somebody asserting something.

Two caveats travel with every reading and must never be dropped:

1. The feed updates weekly with a lag of roughly a week to ten days, so the newest row is
   not today. `lag_days` is reported alongside the value.
2. Current Hormuz counts are extraordinarily low. That is consistent with AIS jamming and
   dark-vessel behaviour in the strait, which makes the series a measure of *observed*
   transits, not of all transits. Plotting it naively as traffic would be wrong.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from typing import Any
from urllib.parse import urlencode

from ..http import HttpClient
from ..models import stable_id

SERVICE = (
    "https://services9.arcgis.com/weJ1QsnbMYJlCHdG/ArcGIS/rest/services/"
    "Daily_Chokepoints_Data/FeatureServer/0/query"
)

# PortWatch's identifier for the Strait of Hormuz.
HORMUZ = "chokepoint6"


def _number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_date(value: Any) -> str:
    """PortWatch returns ISO date strings; older service versions returned epoch millis."""
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, UTC).date().isoformat()
    text = str(value or "").strip()
    return text[:10]


@dataclass(slots=True)
class ChokepointDay:
    chokepoint_id: str
    chokepoint_name: str
    date: str
    n_total: float | None
    n_tanker: float | None
    n_cargo: float | None
    n_container: float | None
    n_dry_bulk: float | None
    n_general_cargo: float | None
    n_roro: float | None
    capacity: float | None
    capacity_tanker: float | None
    capacity_cargo: float | None
    source: str = "imf_portwatch"
    source_url: str = "https://portwatch.imf.org/"

    @property
    def id(self) -> str:
        return stable_id("portwatch", self.chokepoint_id, self.date)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, **asdict(self)}


def parse_features(payload: Any, chokepoint_id: str) -> list[ChokepointDay]:
    if not isinstance(payload, dict):
        raise ValueError("unexpected PortWatch response")
    if "error" in payload:
        raise ValueError(f"PortWatch returned an error: {payload['error']}")
    rows: list[ChokepointDay] = []
    for feature in payload.get("features") or []:
        attributes = (feature or {}).get("attributes") or {}
        day = _as_date(attributes.get("date"))
        if not day:
            continue
        rows.append(
            ChokepointDay(
                chokepoint_id=str(attributes.get("portid") or chokepoint_id),
                chokepoint_name=str(attributes.get("portname") or ""),
                date=day,
                n_total=_number(attributes.get("n_total")),
                n_tanker=_number(attributes.get("n_tanker")),
                n_cargo=_number(attributes.get("n_cargo")),
                n_container=_number(attributes.get("n_container")),
                n_dry_bulk=_number(attributes.get("n_dry_bulk")),
                n_general_cargo=_number(attributes.get("n_general_cargo")),
                n_roro=_number(attributes.get("n_roro")),
                capacity=_number(attributes.get("capacity")),
                capacity_tanker=_number(attributes.get("capacity_tanker")),
                capacity_cargo=_number(attributes.get("capacity_cargo")),
            )
        )
    rows.sort(key=lambda r: r.date)
    return rows


def lag_days(rows: list[dict[str, Any]], *, today: date | None = None) -> int | None:
    """How stale the newest observation is. Surfaced next to every reading."""
    dates = [str(r.get("date", "")) for r in rows if r.get("date")]
    if not dates:
        return None
    try:
        newest = date.fromisoformat(max(dates))
    except ValueError:
        return None
    return ((today or datetime.now(UTC).date()) - newest).days


def rolling_mean(rows: list[dict[str, Any]], field: str = "n_total", window: int = 7) -> float | None:
    """Mean of the last `window` daily values. Daily counts here are far too noisy to read raw."""
    values = [
        float(r[field])
        for r in sorted(rows, key=lambda r: str(r.get("date", "")))[-window:]
        if r.get(field) is not None
    ]
    return round(sum(values) / len(values), 3) if values else None


class PortWatchCollector:
    def __init__(self, client: HttpClient | None = None) -> None:
        self.client = client or HttpClient()

    def chokepoint(
        self, chokepoint_id: str = HORMUZ, *, limit: int = 400
    ) -> list[ChokepointDay]:
        query = urlencode(
            {
                "where": f"portid='{chokepoint_id}'",
                "outFields": "*",
                "orderByFields": "date DESC",
                "resultRecordCount": min(max(limit, 1), 2000),
                "f": "json",
            }
        )
        payload = self.client.get_json(f"{SERVICE}?{query}")
        return parse_features(payload, chokepoint_id)
