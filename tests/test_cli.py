from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from support import FakeClient, MemoryStore

from moscow_watch.cli import (
    _collect_kalshi,
    _collect_polymarket,
    _refresh_legacy_terminal_readings,
)
from moscow_watch.config import Config, Indicator
from moscow_watch.health import SourceHealth
from moscow_watch.tracker import Reading


class LegacyTerminalReadingTests(unittest.TestCase):
    def _config(self, source: str) -> Config:
        indicator = Indicator(
            id="market",
            name="Market",
            source=source,
            kind="market_ladder" if source == "polymarket" else "market_probability",
            event_slug="event" if source == "polymarket" else "",
            series_ticker="SERIES" if source == "kalshi" else "",
            material_move=0.05,
            bears_on=[{"hypothesis": "h1", "direction": "up"}],
        )
        return Config(
            project={}, hypotheses=[], indicators=[indicator], news_sources=[],
            discovery_queries=[], claim_rules=[],
        )

    def test_no_open_polymarket_response_becomes_terminal_not_unavailable(self):
        history = [
            {
                "indicator_id": "market", "name": "Market", "source": "polymarket",
                "kind": "market_ladder", "value": 0.001, "display": "0.1%",
                "collected_at": "2026-08-30T20:00:00Z", "available": True,
                "components": [
                    {"market_id": "polymarket:leg", "yes_price": 0.001, "no_price": 0.999}
                ],
            }
        ]
        latest = Reading(
            indicator_id="market", name="Market", source="polymarket",
            kind="market_ladder", value=None, display="n/a",
            collected_at="2026-08-31T06:00:00Z", available=False,
            unavailable_reason="no open legs",
        )
        repaired = _refresh_legacy_terminal_readings(
            self._config("polymarket"), history, [latest]
        )[0]
        self.assertTrue(repaired.available)
        self.assertEqual(repaired.lifecycle_status, "resolved")
        self.assertEqual(repaired.outcome, "NO")

    def test_no_priced_kalshi_response_is_pending_terminal_state(self):
        history = [
            {
                "indicator_id": "market", "name": "Market", "source": "kalshi",
                "kind": "market_probability", "value": 0.97, "display": "97.0%",
                "collected_at": "2026-09-05T10:00:00Z", "available": True,
                "components": [
                    {"ticker": "SERIES-OCT", "market_id": "kalshi:SERIES-OCT",
                     "last_price": 0.97}
                ],
            }
        ]
        latest = Reading(
            indicator_id="market", name="Market", source="kalshi",
            kind="market_probability", value=None, display="n/a",
            collected_at="2026-09-05T20:00:00Z", available=False,
            unavailable_reason="series has no priced open markets",
        )
        repaired = _refresh_legacy_terminal_readings(
            self._config("kalshi"), history, [latest]
        )[0]
        self.assertTrue(repaired.available)
        self.assertEqual(repaired.lifecycle_status, "closed")
        self.assertEqual(repaired.market_id, "kalshi:SERIES-OCT")


class TerminalCollectionTests(unittest.TestCase):
    def test_closed_polymarket_event_is_a_successful_resolved_reading(self):
        indicator = Indicator(
            id="market", name="Market", source="polymarket", kind="market_ladder",
            event_slug="event", resolves="2026-09-30", material_move=0.05,
            bears_on=[{"hypothesis": "h1", "direction": "up"}],
        )
        config = Config(
            project={}, hypotheses=[], indicators=[indicator], news_sources=[],
            discovery_queries=[], claim_rules=[],
        )
        payload = [{
            "markets": [{
                "slug": "leg", "conditionId": "condition", "question": "Question?",
                "groupItemTitle": "September 30", "endDate": "2026-09-30T20:29:00Z",
                "outcomes": '["Yes", "No"]', "outcomePrices": '["0", "1"]',
                "closed": True, "active": False,
            }]
        }]
        with tempfile.TemporaryDirectory() as directory:
            with redirect_stdout(StringIO()):
                readings = _collect_polymarket(
                    config,
                    MemoryStore(),
                    SourceHealth(Path(directory) / "health.json"),
                    FakeClient(payload=payload),
                    "2026-10-01T00:00:00Z",
                )
        self.assertTrue(readings[0].available)
        self.assertEqual(readings[0].lifecycle_status, "resolved")
        self.assertEqual(readings[0].outcome, "NO")

    def test_kalshi_rollover_retains_terminal_prior_contract(self):
        indicator = Indicator(
            id="market", name="Market", source="kalshi", kind="market_probability",
            series_ticker="SERIES", material_move=0.05,
            bears_on=[{"hypothesis": "h1", "direction": "up"}],
        )
        config = Config(
            project={}, hypotheses=[], indicators=[indicator], news_sources=[],
            discovery_queries=[], claim_rules=[],
        )
        old = {
            "id": "old", "market_id": "kalshi:SERIES-OCT", "ticker": "SERIES-OCT",
            "series_ticker": "SERIES", "captured_at": "2026-09-05T00:00:00Z",
            "status": "active", "rules_fingerprint": "unchanged",
        }
        open_market = {
            "ticker": "SERIES-JAN", "series_ticker": "SERIES", "title": "January leg",
            "status": "active", "close_time": "2027-01-01T00:00:00Z",
            "last_price_dollars": "0.40", "yes_bid_dollars": "0.39",
        }
        settled_market = {
            "ticker": "SERIES-OCT", "series_ticker": "SERIES", "title": "October leg",
            "status": "settled", "result": "yes", "close_time": "2026-10-01T00:00:00Z",
        }
        client = FakeClient(
            routes={
                "status=open": {"markets": [open_market]},
                "status=settled": {"markets": [settled_market]},
                "status=closed": {"markets": []},
            }
        )
        store = MemoryStore({"kalshi_markets": [old]})
        with tempfile.TemporaryDirectory() as directory:
            with redirect_stdout(StringIO()):
                readings, _ = _collect_kalshi(
                    config,
                    store,
                    SourceHealth(Path(directory) / "health.json"),
                    client,
                    "2026-09-06T00:00:00Z",
                )
        self.assertEqual(readings[0].market_id, "kalshi:SERIES-JAN")
        terminal = next(
            component
            for component in readings[0].components
            if component.get("ticker") == "SERIES-OCT"
        )
        self.assertEqual(terminal["result"], "yes")


if __name__ == "__main__":
    unittest.main()
