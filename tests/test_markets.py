"""Ladder parsing, hazard maths, Kalshi parsing and PortWatch parsing. All offline."""

from __future__ import annotations

import math
import unittest
from datetime import date

from support import fixture_json

from moscow_watch.collectors.kalshi import (
    parse_candlesticks,
    parse_markets,
    parse_settlement_sources,
    rules_changes,
)
from moscow_watch.collectors.polymarket import (
    open_legs,
    parse_event,
    parse_history,
    parse_trades,
    tape_summary,
)
from moscow_watch.collectors.portwatch import lag_days, parse_features, rolling_mean
from moscow_watch.hazard import (
    Rung,
    build_curve,
    forward_conditional,
    hazard_per_day,
    monthly_equivalent,
)

TODAY = date(2026, 8, 26)


class LadderParsingTests(unittest.TestCase):
    def _legs(self):
        return parse_event(
            fixture_json("polymarket_ladder.json"),
            "russia-x-ukraine-ceasefire-agreement-by",
            "2026-08-26T12:00:00Z",
        )

    def test_every_leg_of_the_event_is_returned_not_just_one(self):
        # Reading a single leg cannot distinguish a parallel shift from a shape change.
        self.assertGreaterEqual(len(self._legs()), 5)

    def test_settled_leg_with_no_prices_is_skipped_not_fatal(self):
        slugs = {leg.market_slug for leg in self._legs()}
        self.assertNotIn("cf-jul", slugs, "the priceless settled leg should be dropped")
        self.assertIn("cf-dec", slugs, "and the rest of the ladder must survive")

    def test_open_legs_excludes_closed_and_expired(self):
        live = open_legs(self._legs(), today=TODAY)
        slugs = [leg.market_slug for leg in live]
        self.assertNotIn("cf-jun", slugs)
        self.assertEqual(slugs, ["cf-aug", "cf-oct", "cf-dec", "cf-mar"])

    def test_legs_are_ordered_by_resolution_date(self):
        live = open_legs(self._legs(), today=TODAY)
        dates = [leg.resolves for leg in live]
        self.assertEqual(dates, sorted(dates))

    def test_outcomes_prices_and_tokens_stay_index_aligned(self):
        leg = next(x for x in self._legs() if x.market_slug == "cf-dec")
        self.assertEqual(leg.outcomes, ["Yes", "No"])
        self.assertEqual(leg.yes_price, 0.235)
        self.assertEqual(leg.no_price, 0.765)
        self.assertEqual(leg.token_for("Yes"), "t-dec-y")
        self.assertEqual(leg.token_for("No"), "t-dec-n")

    def test_open_leg_with_mismatched_prices_is_an_error(self):
        payload = fixture_json("polymarket_ladder.json")
        payload[0]["markets"][4]["outcomePrices"] = '["0.235"]'  # open Dec leg
        with self.assertRaisesRegex(ValueError, "outcomes but"):
            parse_event(payload, "slug", "2026-08-26T12:00:00Z")

    def test_history_points_are_tagged_as_backfill(self):
        points = parse_history(fixture_json("polymarket_history.json"), "t-dec-y", "m")
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0].source, "polymarket_prices_history")
        self.assertLess(points[0].timestamp, points[-1].timestamp)

    def test_trade_tape_distinguishes_size_from_price(self):
        trades = parse_trades(fixture_json("polymarket_trades.json"), "c-dec", "m")
        summary = tape_summary([t.to_dict() for t in trades])
        self.assertEqual(summary["trades"], 3)
        # One large fill and two small ones: the median is far below the largest.
        self.assertLess(summary["median_notional"], summary["largest_notional"])
        self.assertAlmostEqual(summary["largest_notional"], 99.98, places=1)


class HazardTests(unittest.TestCase):
    def _rungs(self):
        return [
            Rung("31 Aug", date(2026, 8, 31), 0.0075),
            Rung("31 Oct", date(2026, 10, 31), 0.105),
            Rung("31 Dec", date(2026, 12, 31), 0.235),
            Rung("31 Mar", date(2027, 3, 31), 0.415),
            Rung("30 Jun", date(2027, 6, 30), 0.535),
        ]

    def test_forward_conditional_strips_out_window_length(self):
        # Raw cumulative rises with time; the conditional is what is comparable.
        self.assertAlmostEqual(forward_conditional(0.0, 0.10), 0.10)
        self.assertAlmostEqual(forward_conditional(0.10, 0.20), 0.1111, places=4)

    def test_p_equals_one_leaves_nothing_to_happen(self):
        self.assertEqual(forward_conditional(1.0, 1.0), 0.0)

    def test_p_equals_zero_is_handled(self):
        self.assertEqual(forward_conditional(0.0, 0.0), 0.0)
        self.assertEqual(hazard_per_day(0.0, 30), 0.0)

    def test_non_monotone_ladder_clamps_to_zero_rather_than_going_negative(self):
        # Adjacent legs trade independently, so real quotes are sometimes inverted.
        self.assertEqual(forward_conditional(0.5, 0.3), 0.0)

    def test_certain_conditional_is_infinite_hazard_capped_at_one_monthly(self):
        self.assertTrue(math.isinf(hazard_per_day(1.0, 30)))
        self.assertEqual(monthly_equivalent(hazard_per_day(1.0, 30)), 1.0)

    def test_zero_length_window_is_rejected(self):
        with self.assertRaises(ValueError):
            hazard_per_day(0.5, 0)

    def test_out_of_range_probability_is_rejected(self):
        with self.assertRaises(ValueError):
            forward_conditional(0.0, 1.5)

    def test_short_leg_is_excluded_and_the_exclusion_is_reported(self):
        curve = build_curve(self._rungs(), today=TODAY)
        short = next(p for p in curve.points if p.label == "31 Aug")
        self.assertFalse(short.informative)
        self.assertIn("tick floor", short.excluded_because)
        self.assertIn("31 Aug", curve.excluded)

    def test_curve_shape_identifies_peak_and_trough(self):
        curve = build_curve(self._rungs(), today=TODAY)
        self.assertEqual(curve.peak.label, "31 Mar")
        self.assertEqual(curve.trough.label, "31 Oct")
        # The excluded short leg must not be able to win either.
        self.assertNotIn("31 Aug", [curve.peak.label, curve.trough.label])

    def test_a_rung_at_or_before_today_carries_no_window(self):
        curve = build_curve([Rung("past", date(2026, 8, 20), 0.4)], today=TODAY)
        self.assertFalse(curve.points[0].informative)
        self.assertIn("already closed", curve.points[0].excluded_because)


class KalshiTests(unittest.TestCase):
    def _markets(self, sources=None):
        return parse_markets(
            fixture_json("kalshi_markets.json"), "KXTEST", "2026-08-26T12:00:00Z", sources
        )

    def test_dollar_fields_are_probabilities_and_are_not_rescaled(self):
        market = self._markets()[0]
        self.assertEqual(market.yes_bid, 0.01)
        self.assertEqual(market.yes_ask, 0.08)
        self.assertEqual(market.last_price, 0.10)

    def test_open_interest_and_volume_come_from_the_fp_fields(self):
        market = self._markets()[0]
        self.assertAlmostEqual(market.open_interest, 421.31)
        self.assertAlmostEqual(market.volume, 422.31)

    def test_settlement_sources_are_read_from_the_event(self):
        sources = parse_settlement_sources(fixture_json("kalshi_event.json"))
        self.assertEqual(len(sources), 1)
        self.assertIn("IMF PortWatch", sources[0])
        market = self._markets({"KXTEST-26AUG30": sources})[0]
        self.assertEqual(market.settlement_sources, sources)

    def test_candlesticks_carry_open_interest(self):
        payload = {
            "candlesticks": [
                {
                    "end_period_ts": 1787716800,
                    "open_interest_fp": "217.65",
                    "volume_fp": "12.0",
                    "price": {"open_dollars": "0.07", "high_dollars": "0.07",
                              "low_dollars": "0.02", "close_dollars": "0.02"},
                }
            ]
        }
        candle = parse_candlesticks(payload, "KXTEST")[0]
        self.assertAlmostEqual(candle.open_interest, 217.65)
        self.assertAlmostEqual(candle.close_dollars, 0.02)

    def test_first_sighting_of_a_series_is_not_reported_as_change(self):
        current = [m.to_dict() for m in self._markets()]
        self.assertEqual(rules_changes([], current), [])

    def test_changed_resolution_wording_is_flagged(self):
        before = [m.to_dict() for m in self._markets()]
        payload = fixture_json("kalshi_markets.json")
        payload["markets"][0]["rules_primary"] = "Completely different settlement rule."
        after = [
            m.to_dict()
            for m in parse_markets(payload, "KXTEST", "2026-08-27T12:00:00Z")
        ]
        changes = rules_changes(before, after)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]["kind"], "rules_changed")
        self.assertIn("different settlement", changes[0]["after"])

    def test_new_market_in_a_tracked_series_is_flagged(self):
        before = [m.to_dict() for m in self._markets()][:1]
        after = [m.to_dict() for m in self._markets()]
        changes = rules_changes(before, after)
        self.assertEqual([c["kind"] for c in changes], ["new_market"])


class PortWatchTests(unittest.TestCase):
    def _rows(self):
        return [r.to_dict() for r in parse_features(fixture_json("portwatch.json"), "chokepoint6")]

    def test_rows_parse_with_iso_dates_and_counts(self):
        rows = self._rows()
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[-1]["date"], "2026-08-23")
        self.assertEqual(rows[-1]["n_total"], 3.0)
        self.assertEqual(rows[-1]["chokepoint_name"], "Strait of Hormuz")

    def test_rows_are_returned_oldest_first(self):
        dates = [r["date"] for r in self._rows()]
        self.assertEqual(dates, sorted(dates))

    def test_lag_is_reported_so_the_feed_is_never_read_as_current(self):
        self.assertEqual(lag_days(self._rows(), today=date(2026, 9, 2)), 10)

    def test_rolling_mean_smooths_a_very_noisy_daily_count(self):
        self.assertAlmostEqual(rolling_mean(self._rows(), "n_total", window=3), 4.667, places=2)

    def test_an_arcgis_error_payload_is_a_readable_failure(self):
        with self.assertRaisesRegex(ValueError, "PortWatch returned an error"):
            parse_features(fixture_json("portwatch_error.json"), "chokepoint6")


if __name__ == "__main__":
    unittest.main()
