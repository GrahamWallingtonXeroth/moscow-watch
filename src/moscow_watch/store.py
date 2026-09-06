from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

try:
    import fcntl
except ImportError:  # pragma: no cover - the scheduled collector runs on Linux
    fcntl = None  # type: ignore[assignment]


class JsonlStore:
    """A transparent, append-only store designed to produce readable git diffs."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, name: str) -> Path:
        return self.root / f"{name}.jsonl"

    def read(self, name: str) -> list[dict[str, Any]]:
        target = self.path(name)
        if not target.exists():
            return []
        records: list[dict[str, Any]] = []
        with target.open("r", encoding="utf-8") as handle:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"invalid JSON in {target}:{line_number}") from exc
        return records

    def append_unique(
        self,
        name: str,
        records: Iterable[dict[str, Any]],
        *,
        key: str = "id",
    ) -> int:
        target = self.path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        # The workflow can be triggered by both its schedule and a nearby push. Lock the
        # read-check-write sequence so two collectors cannot both decide the same id is
        # absent and append it. The in-process `existing.add` also deduplicates one API
        # response containing the same observation more than once.
        with target.open("a+", encoding="utf-8") as handle:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            handle.seek(0)
            existing: set[Any] = set()
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    existing.add(json.loads(line).get(key))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"invalid JSON in {target}:{line_number}") from exc
            additions: list[dict[str, Any]] = []
            for item in records:
                value = item.get(key)
                if value in existing:
                    continue
                additions.append(item)
                existing.add(value)
            if not additions:
                return 0
            handle.seek(0, 2)
            for item in additions:
                handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
            handle.flush()
        return len(additions)
