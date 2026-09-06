from __future__ import annotations

import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor

from moscow_watch.store import JsonlStore


class JsonlStoreTests(unittest.TestCase):
    def test_duplicate_ids_within_one_batch_are_written_once(self):
        with tempfile.TemporaryDirectory() as directory:
            store = JsonlStore(directory)
            added = store.append_unique(
                "daily",
                [
                    {"id": "day:2026-09-01", "value": 0.1},
                    {"id": "day:2026-09-01", "value": 0.9},
                ],
            )
            self.assertEqual(added, 1)
            self.assertEqual(store.read("daily"), [{"id": "day:2026-09-01", "value": 0.1}])

    def test_concurrent_writers_cannot_append_the_same_id_twice(self):
        with tempfile.TemporaryDirectory() as directory:
            stores = [JsonlStore(directory), JsonlStore(directory)]
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(
                    pool.map(
                        lambda store: store.append_unique(
                            "daily", [{"id": "day:2026-09-01", "value": 0.1}]
                        ),
                        stores,
                    )
                )
            self.assertEqual(sum(results), 1)
            self.assertEqual(len(stores[0].read("daily")), 1)


if __name__ == "__main__":
    unittest.main()
