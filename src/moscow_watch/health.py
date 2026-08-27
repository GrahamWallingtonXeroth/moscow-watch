from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import SourceStatus, hours_since, is_stale, utc_now_iso


class SourceHealth:
    """Current state per source, overwritten in place.

    A permanently broken feed must not append a new row every six hours forever, so this
    is a keyed document rather than an append-only ledger.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.entries: dict[str, SourceStatus] = {}
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                raw = {}
            for key, value in (raw.get("sources") or {}).items():
                known = {field for field in SourceStatus.__dataclass_fields__}
                self.entries[key] = SourceStatus(
                    **{k: v for k, v in value.items() if k in known}
                )

    def _entry(
        self, source_id: str, kind: str, label: str, target: str, source_family: str = ""
    ) -> SourceStatus:
        entry = self.entries.get(source_id)
        if entry is None:
            entry = SourceStatus(source_id=source_id, kind=kind, label=label, target=target)
            self.entries[source_id] = entry
        entry.kind, entry.label, entry.target = kind, label, target
        if source_family:
            entry.source_family = source_family
        return entry

    def record_success(
        self,
        source_id: str,
        *,
        kind: str,
        label: str,
        target: str,
        records: int,
        at: str,
        source_family: str = "",
    ) -> None:
        entry = self._entry(source_id, kind, label, target, source_family)
        entry.status = "ok"
        entry.last_attempt_at = at
        entry.last_success_at = at
        entry.records = records
        entry.error_category = ""
        entry.error_message = ""
        entry.consecutive_failures = 0

    def record_failure(
        self,
        source_id: str,
        *,
        kind: str,
        label: str,
        target: str,
        category: str,
        message: str,
        at: str,
        source_family: str = "",
    ) -> None:
        entry = self._entry(source_id, kind, label, target, source_family)
        entry.status = "failed"
        entry.last_attempt_at = at
        entry.records = 0
        entry.error_category = category
        entry.error_message = message[:300]
        entry.consecutive_failures += 1

    def record_disabled(
        self,
        source_id: str,
        *,
        kind: str,
        label: str,
        target: str,
        reason: str,
        source_family: str = "",
    ) -> None:
        entry = self._entry(source_id, kind, label, target, source_family)
        entry.status = "disabled"
        entry.error_category = "disabled"
        entry.error_message = reason[:300]
        entry.records = 0

    def apply_staleness(self, threshold_hours: float, *, now: datetime | None = None) -> None:
        for entry in self.entries.values():
            if entry.status == "ok" and is_stale(entry.last_success_at, threshold_hours, now=now):
                entry.status = "stale"

    def summary(self, threshold_hours: float, *, now: datetime | None = None) -> dict[str, Any]:
        by_status: dict[str, int] = {}
        for entry in self.entries.values():
            by_status[entry.status] = by_status.get(entry.status, 0) + 1

        # Each evidence layer is reported separately: losing all newsrooms is a different
        # failure from losing the discovery index, and only one of them stops scoring.
        layers: dict[str, dict[str, Any]] = {}
        for layer in (
            "polymarket",
            "kalshi",
            "portwatch",
            "independent_reporting",
            "primary_record",
            "discovery",
            "gdelt",
        ):
            entries = [e for e in self.entries.values() if e.kind == layer]
            ok = [e for e in entries if e.status == "ok"]
            families_ok = {e.source_family for e in ok if e.source_family}
            successes = [e.last_success_at for e in entries if e.last_success_at]
            layers[layer] = {
                "configured": len(entries),
                "ok": len(ok),
                "failed": len([e for e in entries if e.status == "failed"]),
                "disabled": len([e for e in entries if e.status == "disabled"]),
                "families_ok": len(families_ok),
                "families": sorted(families_ok),
                "last_success_at": max(successes) if successes else "",
            }

        market = layers["polymarket"]
        reporting = layers["independent_reporting"]
        successes = [
            e.last_success_at
            for e in self.entries.values()
            if e.kind in {"polymarket", "independent_reporting"} and e.last_success_at
        ]
        newest = max(successes) if successes else ""
        stale = is_stale(newest, threshold_hours, now=now) if newest else True

        if not market["configured"] or market["ok"] == 0:
            overall = "unavailable"
        elif reporting["families_ok"] < 2:
            # Fewer than two independent families means nothing can be corroborated.
            overall = "partial"
        elif stale:
            overall = "stale"
        elif market["ok"] < market["configured"] or reporting["ok"] < reporting["configured"]:
            overall = "partial"
        else:
            overall = "ok"

        return {
            "overall": overall,
            "core_sources": market["configured"] + reporting["configured"],
            "core_sources_ok": market["ok"] + reporting["ok"],
            "newest_core_success_at": newest,
            "age_hours": round(hours_since(newest, now=now) or 0.0, 2) if newest else None,
            "stale_after_hours": threshold_hours,
            "corroboration_possible": reporting["families_ok"] >= 2,
            "layers": layers,
            "by_status": by_status,
        }

    def write(self, threshold_hours: float, *, now: datetime | None = None) -> dict[str, Any]:
        self.apply_staleness(threshold_hours, now=now)
        document = {
            "updated_at": utc_now_iso(),
            "summary": self.summary(threshold_hours, now=now),
            "sources": {key: value.to_dict() for key, value in sorted(self.entries.items())},
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return document

    def document(self, threshold_hours: float, *, now: datetime | None = None) -> dict[str, Any]:
        self.apply_staleness(threshold_hours, now=now)
        return {
            "updated_at": utc_now_iso(),
            "summary": self.summary(threshold_hours, now=now),
            "sources": {key: value.to_dict() for key, value in sorted(self.entries.items())},
        }
