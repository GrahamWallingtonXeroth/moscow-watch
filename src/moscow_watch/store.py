from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


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
        existing = {item.get(key) for item in self.read(name)}
        additions = [item for item in records if item.get(key) not in existing]
        if not additions:
            return 0
        target = self.path(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as handle:
            for item in additions:
                handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
        return len(additions)
