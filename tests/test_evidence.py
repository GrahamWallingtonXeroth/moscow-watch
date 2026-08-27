"""Corroboration, duplicate clustering, contact counting and change suppression."""

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import UTC, date, datetime

from support import CountingSleeper, FakeClient, fixture, fixture_json

from moscow_watch.collectors.contacts import (
    baseline,
    direction,
    extract_contacts,
    fortnight_start,
    fortnightly_series,
)
from moscow_watch.collectors.feeds import NewsFeedCollector
from moscow_watch.collectors.gdelt import GdeltDiscovery, GdeltVolumeTimeline
from moscow_watch.config import (
    ClaimRule,
    Config,
    DiscoveryQuery,
    Indicator,
    NewsSource,
    load_config,
    validate_config,
)
from moscow_watch.corroboration import attested, leads, promote_claims
from moscow_watch.dedupe import group_duplicates, is_near_duplicate
from moscow_watch.diff import count_suppressed, find_movements
from moscow_watch.engagement import (
    axis_position,
    fortnightly_volume,
)
from moscow_watch.engagement import (
    baseline as volume_baseline,
)
from moscow_watch.engagement import (
    direction as volume_direction,
)
from moscow_watch.matching import detect_negation, match_groups

NOW = datetime(2026, 8, 26, 18, 0, tzinfo=UTC)

GUARDIAN = NewsSource(
    id="guardian", title="Guardian", url="https://www.theguardian.com/world/rss",
    publisher="The Guardian", source_family="guardian",
)
BBC = NewsSource(
    id="bbc", title="BBC", url="https://feeds.bbci.co.uk/news/world/rss.xml",
    publisher="BBC News", source_family="bbc",
)
NPR = NewsSource(
    id="npr", title="NPR", url="https://feeds.npr.org/1004/rss.xml",
    publisher="NPR", source_family="npr",
)
KREMLIN = NewsSource(
    id="kremlin", title="Kremlin", url="http://en.kremlin.ru/events/president/news/feed",
    publisher="Kremlin", source_family="kremlin", source_type="primary_record",
    standpoint="Russian presidential administration",
)
WHITEHOUSE = NewsSource(
    id="wh", title="White House", url="https://www.whitehouse.gov/news/feed/",
    publisher="The White House", source_family="us_executive",
    source_type="primary_record", standpoint="United States executive branch",
)

SUPPORT = ClaimRule(
    id="russia_iran_support_down", title="Russia reduces support", hypothesis_id="h3",
    claim_type="external_observable",
    required_groups=[["russia", "moscow"], ["iran"], ["halt", "halts", "stop", "stopped"],
                     ["weapons", "intelligence"]],
)
SANCTIONS = ClaimRule(
    id="us_costs", title="US imposes costs", hypothesis_id="h5", claim_type="official_action",
    required_groups=[["russia"], ["united states", "treasury"], ["sanctions"],
                     ["imposes", "new", "imposed"]],
)


def config_with(rules, indicators=()):
    return Config(
        project={}, hypotheses=[], indicators=list(indicators),
        news_sources=[], discovery_queries=[], claim_rules=list(rules),
    )


def collect(source, name):
    client = FakeClient(text=fixture(name))
    return [i.to_dict() for i in NewsFeedCollector(client).collect(source, window_hours=72, now=NOW)]


class PromotionTests(unittest.TestCase):
    def test_two_independent_families_attest_one_claim(self):
        items = collect(GUARDIAN, "feed_guardian.xml") + collect(BBC, "feed_bbc.xml")
        claims = promote_claims(config_with([SUPPORT]), items)
        matching = [c for c in claims if c["signal_id"] == SUPPORT.id]
        self.assertEqual(len(matching), 1, "one story yields one claim")
        self.assertEqual(matching[0]["corroboration_status"], "corroborated")
        self.assertEqual(sorted(matching[0]["source_families"]), ["bbc", "guardian"])

    def test_single_family_is_only_a_lead(self):
        claims = promote_claims(config_with([SUPPORT]), collect(GUARDIAN, "feed_guardian.xml"))
        claim = [c for c in claims if c["signal_id"] == SUPPORT.id][0]
        self.assertEqual(claim["corroboration_status"], "single_source")
        self.assertIn(claim, leads(claims))
        self.assertNotIn(claim, attested(claims))

    def test_discovery_alone_can_never_attest(self):
        client = FakeClient(payload=fixture_json("gdelt_discovery.json"))
        found = [
            i.to_dict()
            for i in GdeltDiscovery(client, sleeper=CountingSleeper()).collect(
                DiscoveryQuery(id="d", title="D", query="q"), window_hours=72
            )
        ]
        claims = promote_claims(config_with([SUPPORT]), found)
        self.assertTrue(claims)
        for claim in claims:
            self.assertEqual(claim["corroboration_status"], "discovery_only")
        self.assertEqual(attested(claims), [])

    def test_discovery_plus_one_newsroom_is_still_a_lead(self):
        client = FakeClient(payload=fixture_json("gdelt_discovery.json"))
        found = [
            i.to_dict()
            for i in GdeltDiscovery(client, sleeper=CountingSleeper()).collect(
                DiscoveryQuery(id="d", title="D", query="q"), window_hours=72
            )
        ]
        claims = promote_claims(
            config_with([SUPPORT]), collect(GUARDIAN, "feed_guardian.xml") + found
        )
        claim = [c for c in claims if c["signal_id"] == SUPPORT.id][0]
        self.assertEqual(claim["corroboration_status"], "single_source")

    def test_official_action_is_documented_by_a_primary_record(self):
        claims = promote_claims(
            config_with([SANCTIONS]), collect(WHITEHOUSE, "feed_primary_whitehouse.xml")
        )
        claim = [c for c in claims if c["signal_id"] == SANCTIONS.id][0]
        self.assertEqual(claim["corroboration_status"], "primary_documented")
        self.assertIn(claim, attested(claims))

    def test_primary_record_carries_its_standpoint(self):
        items = collect(KREMLIN, "feed_primary_kremlin.xml")
        self.assertEqual(items[0]["standpoint"], "Russian presidential administration")

    def test_opposing_rules_make_a_story_contested(self):
        mirror = ClaimRule(
            id="mirror", title="mirror", hypothesis_id="h3", claim_type="external_observable",
            required_groups=SUPPORT.required_groups, verdict="against",
        )
        rule = replace(SUPPORT, verdict="toward")
        items = collect(GUARDIAN, "feed_guardian.xml") + collect(BBC, "feed_bbc.xml")
        claims = promote_claims(config_with([rule, mirror]), items)
        contested = [c for c in claims if c["corroboration_status"] == "contested"]
        self.assertEqual(len(contested), 1)
        self.assertEqual(attested(claims), [])

    def test_no_claim_carries_a_numeric_contribution(self):
        items = collect(GUARDIAN, "feed_guardian.xml") + collect(BBC, "feed_bbc.xml")
        for claim in promote_claims(config_with([SUPPORT]), items):
            self.assertNotIn("contribution", claim)
            self.assertNotIn("confidence", claim)

    def test_claim_ids_are_stable_across_runs(self):
        items = collect(GUARDIAN, "feed_guardian.xml") + collect(BBC, "feed_bbc.xml")
        config = config_with([SUPPORT])
        self.assertEqual(
            {c["id"] for c in promote_claims(config, items)},
            {c["id"] for c in promote_claims(config, items)},
        )


class DedupeTests(unittest.TestCase):
    def test_syndicated_copies_cluster(self):
        self.assertTrue(is_near_duplicate(
            "Russia halts weapons shipments to Iran, officials say",
            "Russia halts weapons shipments to Iran",
        ))

    def test_unrelated_headlines_do_not_cluster(self):
        self.assertFalse(is_near_duplicate(
            "Russia halts weapons shipments to Iran",
            "Ukraine ceasefire talks resume in Geneva",
        ))

    def test_grouping_splits_distinct_stories(self):
        groups = group_duplicates([
            {"url": "https://a/1", "title": "Russia halts weapons shipments to Iran"},
            {"url": "https://b/2", "title": "Russia halts weapons shipments to Iran, officials say"},
            {"url": "https://c/3", "title": "Oil prices fall on demand worries"},
        ])
        self.assertEqual(sorted(len(g) for g in groups), [1, 2])


class MatchingTests(unittest.TestCase):
    def test_denial_blocks_a_match(self):
        text = "Moscow denies halting weapons and intelligence support to Iran"
        self.assertTrue(detect_negation(text))
        self.assertFalse(match_groups(text, SUPPORT.required_groups)[0])

    def test_plain_report_matches(self):
        self.assertTrue(match_groups(
            "Russia halts weapons shipments and intelligence sharing with Iran",
            SUPPORT.required_groups,
        )[0])

    def test_whole_word_rejects_substring(self):
        self.assertFalse(match_groups("Nonstop flights resume", [["stop"]])[0])

    def test_incomplete_group_does_not_match(self):
        self.assertFalse(match_groups("Russia and Iran discuss trade", SUPPORT.required_groups)[0])


class ContactCounterTests(unittest.TestCase):
    def _items(self):
        return [
            {"title": "Lavrov meets Iranian foreign minister Araghchi in Moscow for talks",
             "summary": "", "url": "https://a/1", "published_at": "2026-08-20T10:00:00Z",
             "publisher": "Guardian", "source_family": "guardian",
             "source_type": "independent_reporting"},
            {"title": "Russia and Iran hold consultations on nuclear file",
             "summary": "Deputy foreign minister Ryabkov led the delegation.",
             "url": "https://b/2", "published_at": "2026-08-22T10:00:00Z",
             "publisher": "BBC", "source_family": "bbc", "source_type": "independent_reporting"},
            {"title": "Oil prices fall on demand worries", "summary": "",
             "url": "https://c/3", "published_at": "2026-08-23T10:00:00Z",
             "publisher": "NPR", "source_family": "npr", "source_type": "independent_reporting"},
        ]

    def test_only_genuine_contacts_are_counted(self):
        contacts = extract_contacts(self._items())
        self.assertEqual(len(contacts), 2)
        self.assertTrue(all(c.url for c in contacts), "every contact keeps its source URL")

    def test_seniority_is_recorded(self):
        contacts = extract_contacts(self._items())
        self.assertTrue(any(c.senior for c in contacts))

    def test_recollection_never_double_counts(self):
        items = self._items()
        first = {c.id for c in extract_contacts(items)}
        second = {c.id for c in extract_contacts(items + items)}
        self.assertEqual(first, second)

    def test_fortnight_bucketing_is_anchored(self):
        anchor = date(2026, 1, 5)
        self.assertEqual(fortnight_start(date(2026, 1, 5), anchor=anchor), anchor)
        self.assertEqual(fortnight_start(date(2026, 1, 18), anchor=anchor), anchor)
        self.assertEqual(fortnight_start(date(2026, 1, 19), anchor=anchor), date(2026, 1, 19))

    def test_series_and_baseline_and_direction(self):
        contacts = [c.to_dict() for c in extract_contacts(self._items())]
        series = fortnightly_series(contacts, anchor=date(2026, 1, 5))
        self.assertEqual(sum(b["count"] for b in series), 2)
        self.assertTrue(all(b["citations"] for b in series))
        base = baseline(series, before=date(2026, 12, 1))
        self.assertEqual(base["fortnights"], len(series))
        self.assertEqual(direction([], {"mean_per_fortnight": None}), "insufficient data")


class SuppressionTests(unittest.TestCase):
    """`material_move` and the minimum window are the anti-noise guarantees."""

    def _config(self, material_move=0.05, min_window=6.0):
        indicator = Indicator(
            id="ind", name="Test", source="kalshi", kind="market_probability",
            material_move=material_move, bears_on=[{"hypothesis": "h1", "direction": "up"}],
        )
        return Config(
            project={"min_change_window_hours": min_window}, hypotheses=[],
            indicators=[indicator], news_sources=[], discovery_queries=[], claim_rules=[],
        )

    def _history(self, before, after, hours):
        return [
            {"indicator_id": "ind", "value": before, "collected_at": "2026-08-26T00:00:00Z",
             "available": True},
            {"indicator_id": "ind", "value": after,
             "collected_at": f"2026-08-26T{hours:02d}:00:00Z", "available": True},
        ]

    def test_a_big_move_over_a_long_window_is_reported(self):
        moves = find_movements(self._config(), self._history(0.20, 0.30, 12), since="2026-08-01")
        self.assertEqual(len(moves), 1)
        self.assertAlmostEqual(moves[0].change, 0.10)
        self.assertIn("pts", moves[0].display_change)

    def test_a_move_below_material_move_is_suppressed(self):
        config = self._config(material_move=0.05)
        history = self._history(0.20, 0.22, 12)
        self.assertEqual(find_movements(config, history, since="2026-08-01"), [])
        self.assertEqual(count_suppressed(config, history, since="2026-08-01"), 1)

    def test_a_move_over_too_short_a_window_is_suppressed(self):
        # A half-point move over a three-minute window is noise, not news.
        config = self._config(min_window=6.0)
        history = self._history(0.20, 0.40, 3)
        self.assertEqual(find_movements(config, history, since="2026-08-01"), [])
        self.assertEqual(count_suppressed(config, history, since="2026-08-01"), 1)

    def test_an_unchanged_indicator_is_not_counted_as_suppressed(self):
        config = self._config()
        self.assertEqual(count_suppressed(config, self._history(0.2, 0.2, 12), since="2026-08-01"), 0)

    def test_unavailable_readings_are_ignored(self):
        config = self._config()
        history = self._history(0.20, 0.40, 12)
        history[1]["available"] = False
        self.assertEqual(find_movements(config, history, since="2026-08-01"), [])


class ShippedConfigTests(unittest.TestCase):
    def test_indicators_toml_is_valid(self):
        self.assertEqual(validate_config(load_config("indicators.toml")), [])

    def test_every_indicator_bears_on_a_known_hypothesis(self):
        config = load_config("indicators.toml")
        ids = {h.id for h in config.hypotheses}
        for indicator in config.indicators:
            self.assertTrue(indicator.bears_on, indicator.id)
            for bearing in indicator.bearings:
                self.assertIn(bearing.hypothesis, ids)

    def test_every_tracked_hypothesis_states_a_falsifier_and_a_date(self):
        for hypothesis in load_config("indicators.toml").hypotheses:
            if hypothesis.scored:
                self.assertTrue(hypothesis.falsifier, hypothesis.id)
                self.assertTrue(hypothesis.falsifier_date, hypothesis.id)

    def test_h4_is_falsified_by_a_flat_reading_not_only_by_a_fall(self):
        # H4 predicts that Russian engagement RISES, because carrying a message means
        # travelling. A falsifier phrased as "a fall below baseline" lets a flat reading
        # survive a hypothesis it should kill.
        h4 = load_config("indicators.toml").hypothesis("h4")
        self.assertIn("have not risen above", h4.falsifier)
        self.assertNotIn("A fall in", h4.falsifier)

    def test_the_reporting_index_says_it_is_not_a_count_of_contacts(self):
        config = load_config("indicators.toml")
        indicator = next(i for i in config.indicators if i.source == "gdelt")
        self.assertEqual(indicator.name, "Russia-Iran engagement volume (reporting index)")
        self.assertTrue(indicator.query, "a volume series is defined by its query")
        note = indicator.note.casefold()
        self.assertIn("reporting volume", note)
        self.assertIn("rather than a count of contacts", note)
        self.assertIn("attest", note)
        self.assertIn("direction", note)

    def test_the_directly_collected_contact_counter_is_still_tracked(self):
        config = load_config("indicators.toml")
        counter = next(i for i in config.indicators if i.id == "russia_iran_contacts")
        self.assertEqual(counter.source, "corpus")

    def test_a_gdelt_indicator_without_a_query_is_caught(self):
        config = load_config("indicators.toml")
        next(i for i in config.indicators if i.source == "gdelt").query = ""
        self.assertTrue(any("states no query" in e for e in validate_config(config)))

    def test_untracked_hypothesis_states_why(self):
        h7 = load_config("indicators.toml").hypothesis("h7")
        self.assertFalse(h7.scored)
        self.assertIn("no prediction market", h7.note)

    def test_invalid_direction_is_caught(self):
        config = load_config("indicators.toml")
        config.indicators[0].bears_on = [{"hypothesis": "h1", "direction": "sideways"}]
        self.assertTrue(any("invalid direction" in e for e in validate_config(config)))

    def test_indicator_bearing_on_nothing_is_caught(self):
        config = load_config("indicators.toml")
        config.indicators[0].bears_on = []
        self.assertTrue(any("bears on no hypothesis" in e for e in validate_config(config)))

    def test_out_of_range_material_move_is_caught(self):
        config = load_config("indicators.toml")
        config.indicators[0].material_move = 0
        self.assertTrue(any("material_move" in e for e in validate_config(config)))

    def test_disabled_indicator_must_say_why(self):
        config = load_config("indicators.toml")
        config.indicators[0].enabled = False
        self.assertTrue(any("disabled_reason" in e for e in validate_config(config)))



class ReportingVolumeTests(unittest.TestCase):
    """The GDELT reporting-volume index: what it measures and what it refuses to say."""

    def _points(self):
        client = FakeClient(payload=fixture_json("gdelt_timelinevol.json"))
        timeline = GdeltVolumeTimeline(client, sleeper=CountingSleeper())
        return timeline.volume(
            "(Russia) (Iran) (talks)", start=date(2026, 1, 5), end=date(2026, 1, 20)
        ), client

    def test_timelinevol_mode_and_window_are_requested(self):
        _, client = self._points()
        url = client.calls[0]
        self.assertIn("mode=timelinevol", url)
        self.assertIn("startdatetime=20260105000000", url)
        self.assertIn("enddatetime=20260120235959", url)

    def test_unparseable_rows_are_dropped_not_guessed(self):
        points, _ = self._points()
        self.assertEqual([p.day for p in points],
                         ["2026-01-05", "2026-01-06", "2026-01-07", "2026-01-19"])

    def test_throttle_reply_is_an_error_not_a_series(self):
        client = FakeClient(text=fixture("gdelt_rate_limited.txt"))
        with self.assertRaises(Exception) as caught:
            GdeltVolumeTimeline(client, sleeper=CountingSleeper()).volume(
                "q", start=date(2026, 1, 1), end=date(2026, 1, 2)
            )
        self.assertEqual(getattr(caught.exception, "category", ""), "rate_limited")

    def test_an_empty_timeline_raises_rather_than_returning_nothing(self):
        client = FakeClient(payload={"timeline": [{"series": "Volume Intensity", "data": []}]})
        with self.assertRaises(Exception) as caught:
            GdeltVolumeTimeline(client, sleeper=CountingSleeper()).volume(
                "q", start=date(2026, 1, 1), end=date(2026, 1, 2)
            )
        self.assertEqual(getattr(caught.exception, "category", ""), "empty_timeline")

    def test_days_are_bucketed_into_fortnights_with_their_day_count(self):
        points, _ = self._points()
        series = fortnightly_volume(
            [p.to_dict() for p in points], anchor=date(2026, 1, 5)
        )
        self.assertEqual([b["fortnight_start"] for b in series],
                         ["2026-01-05", "2026-01-19"])
        self.assertAlmostEqual(series[0]["mean_volume"], 0.3)
        self.assertEqual(series[0]["days"], 3)

    def test_days_before_the_event_are_excluded_from_the_live_series(self):
        points = [
            {"day": "2026-08-24", "value": 9.0},
            {"day": "2026-08-25", "value": 0.5},
        ]
        series = fortnightly_volume(
            points, anchor=date(2026, 8, 25), since=date(2026, 8, 25)
        )
        self.assertEqual(len(series), 1)
        self.assertEqual(series[0]["fortnight_start"], "2026-08-25")
        self.assertEqual(series[0]["days"], 1)

    def test_baseline_uses_only_fortnights_ending_before_the_event(self):
        series = [
            {"fortnight_start": "2026-08-03", "fortnight_end": "2026-08-16",
             "mean_volume": 0.2, "days": 14},
            {"fortnight_start": "2026-08-17", "fortnight_end": "2026-08-30",
             "mean_volume": 9.0, "days": 14},
        ]
        base = volume_baseline(series, before=date(2026, 8, 25))
        self.assertEqual(base["fortnights"], 1)
        self.assertAlmostEqual(base["mean_volume"], 0.2)

    def test_no_baseline_means_no_direction_and_no_marker(self):
        base = volume_baseline([], before=date(2026, 8, 25))
        self.assertIsNone(base["mean_volume"])
        series = [{"fortnight_start": "2026-08-25", "mean_volume": 0.5, "days": 14}]
        self.assertEqual(volume_direction(series, base), "insufficient data")
        self.assertIsNone(axis_position(series, base))

    def test_direction_is_relative_because_the_level_means_nothing(self):
        base = {"mean_volume": 0.40, "fortnights": 15}
        self.assertEqual(
            volume_direction([{"mean_volume": 0.60, "days": 14}], base), "up")
        self.assertEqual(
            volume_direction([{"mean_volume": 0.20, "days": 14}], base), "down")
        # Inside the tolerance band a move is not a direction.
        self.assertEqual(
            volume_direction([{"mean_volume": 0.42, "days": 14}], base), "flat")

    def test_marker_is_not_placed_on_less_than_half_a_fortnight(self):
        base = {"mean_volume": 0.40, "fortnights": 15}
        self.assertIsNone(axis_position([{"mean_volume": 0.90, "days": 2}], base))
        self.assertIsNotNone(axis_position([{"mean_volume": 0.90, "days": 7}], base))

    def test_axis_is_clamped_to_the_grid(self):
        base = {"mean_volume": 0.10, "fortnights": 15}
        self.assertEqual(axis_position([{"mean_volume": 9.0, "days": 14}], base), 1.0)
        self.assertEqual(axis_position([{"mean_volume": 0.0, "days": 14}], base), -1.0)



if __name__ == "__main__":
    unittest.main()
