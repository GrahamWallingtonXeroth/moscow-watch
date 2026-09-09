from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import UTC, datetime
from io import StringIO
from pathlib import Path

from support import FakeClient, fixture

from moscow_watch.cli import _collect_analysis_references
from moscow_watch.collectors.sitemaps import (
    SitemapAnalysisCollector,
    assessment_metadata,
    assessment_references,
    recent_post_sitemaps,
)
from moscow_watch.config import AnalysisSource, Config, validate_config
from moscow_watch.diff import render as render_changes
from moscow_watch.health import SourceHealth
from moscow_watch.http import HttpError
from moscow_watch.store import JsonlStore
from moscow_watch.tracker import render as render_tracker


class SitemapAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = AnalysisSource(
            id="isw_russian_offensive_campaign",
            title="ISW Russian Offensive Campaign Assessment",
            url="https://understandingwar.org/sitemap_index.xml",
            publisher="Institute for the Study of War",
            source_family="isw",
            path_prefix=(
                "/research/russia-ukraine/"
                "russian-offensive-campaign-assessment-"
            ),
            rights_url="https://understandingwar.org/fair-use-and-attribution-policy/",
            max_items=7,
        )
        self.now = datetime(2026, 9, 9, 7, tzinfo=UTC)

    def test_metadata_is_derived_from_dated_url(self):
        result = assessment_metadata(
            "https://understandingwar.org/research/russia-ukraine/"
            "russian-offensive-campaign-assessment-september-8-2026/"
        )
        self.assertEqual(
            result,
            ("Russian Offensive Campaign Assessment, September 8, 2026", datetime(2026, 9, 8).date()),
        )

    def test_collector_reads_only_matching_sitemap_metadata(self):
        client = FakeClient(
            routes={
                "sitemap_index.xml": fixture("isw_sitemap_index.xml"),
                "post-sitemap6.xml": fixture("isw_post_sitemap6.xml"),
                "post-sitemap.xml": fixture("isw_post_sitemap.xml"),
            }
        )
        references = SitemapAnalysisCollector(client).collect(
            self.source,
            window_hours=72,
            now=self.now,
            collected_at="2026-09-09T07:00:00Z",
        )

        self.assertEqual(
            [item.assessment_date for item in references],
            ["2026-09-08", "2026-09-07"],
        )
        target = next(item for item in references if item.assessment_date == "2026-09-08")
        self.assertEqual(
            target.title,
            "Russian Offensive Campaign Assessment, September 8, 2026",
        )
        self.assertEqual(target.sitemap_modified_at, "2026-09-09T03:06:45Z")
        self.assertEqual(target.attribution, "Source: Institute for the Study of War")
        self.assertFalse(hasattr(target, "summary"))
        self.assertEqual(
            client.calls,
            [
                "https://understandingwar.org/sitemap_index.xml",
                "https://understandingwar.org/post-sitemap6.xml",
                "https://understandingwar.org/post-sitemap.xml",
            ],
        )
        self.assertTrue(all("assessment-" not in call for call in client.calls))

    def test_revision_timestamp_changes_record_identity(self):
        original = assessment_references(
            self.source,
            fixture("isw_post_sitemap6.xml"),
            window_hours=72,
            now=self.now,
            collected_at="2026-09-09T07:00:00Z",
        )[0]
        revised_xml = fixture("isw_post_sitemap6.xml").replace(
            "2026-09-09T03:06:45+00:00", "2026-09-09T06:00:00+00:00"
        )
        revised = assessment_references(
            self.source,
            revised_xml,
            window_hours=72,
            now=self.now,
            collected_at="2026-09-09T07:00:00Z",
        )[0]
        self.assertNotEqual(original.id, revised.id)
        self.assertEqual(original.url, revised.url)

    def test_recent_revision_of_older_assessment_is_retained(self):
        xml_text = """<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
          <url>
            <loc>https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-september-1-2026/</loc>
            <lastmod>2026-09-09T06:00:00+00:00</lastmod>
          </url>
        </urlset>
        """
        references = assessment_references(
            self.source,
            xml_text,
            window_hours=72,
            now=self.now,
            collected_at="2026-09-09T07:00:00Z",
        )
        self.assertEqual(len(references), 1)
        self.assertEqual(references[0].assessment_date, "2026-09-01")
        self.assertEqual(references[0].sitemap_modified_at, "2026-09-09T06:00:00Z")

    def test_quiet_source_checks_latest_shards_without_reporting_failure(self):
        shards = recent_post_sitemaps(
            self.source,
            fixture("isw_sitemap_index.xml"),
            window_hours=1,
            now=datetime(2026, 9, 10, 7, tzinfo=UTC),
        )
        self.assertEqual(
            shards,
            [
                "https://understandingwar.org/post-sitemap6.xml",
                "https://understandingwar.org/post-sitemap.xml",
            ],
        )

    def test_one_failed_shard_keeps_other_results_and_exposes_warning(self):
        class PartialClient(FakeClient):
            def get_xml_text(self, url: str) -> str:
                if url.endswith("/post-sitemap.xml"):
                    self.calls.append(url)
                    raise HttpError("network", "scripted shard failure")
                return super().get_xml_text(url)

        client = PartialClient(
            routes={
                "sitemap_index.xml": fixture("isw_sitemap_index.xml"),
                "post-sitemap6.xml": fixture("isw_post_sitemap6.xml"),
            }
        )
        collector = SitemapAnalysisCollector(client)
        references = collector.collect(
            self.source,
            window_hours=72,
            now=self.now,
            collected_at="2026-09-09T07:00:00Z",
        )
        self.assertEqual(
            [item.assessment_date for item in references],
            ["2026-09-08", "2026-09-07"],
        )
        self.assertEqual(len(collector.warnings), 1)
        self.assertIn("post-sitemap.xml", collector.warnings[0])
        self.assertIn("scripted shard failure", collector.warnings[0])

    def test_partial_shard_collection_is_persisted_and_visible_in_health(self):
        class PartialClient(FakeClient):
            def get_xml_text(self, url: str) -> str:
                if url.endswith("/post-sitemap.xml"):
                    self.calls.append(url)
                    raise HttpError("network", "scripted shard failure")
                return super().get_xml_text(url)

        client = PartialClient(
            routes={
                "sitemap_index.xml": fixture("isw_sitemap_index.xml"),
                "post-sitemap6.xml": fixture("isw_post_sitemap6.xml"),
            }
        )
        config = Config(
            project={"news_timespan_hours": 72},
            hypotheses=[],
            indicators=[],
            news_sources=[],
            discovery_queries=[],
            claim_rules=[],
            analysis_sources=[self.source],
        )
        with tempfile.TemporaryDirectory() as directory:
            store = JsonlStore(Path(directory) / "data")
            health = SourceHealth(Path(directory) / "source_status.json")
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                _collect_analysis_references(
                    config,
                    store,
                    health,
                    client,
                    "2026-09-09T07:00:00Z",
                )
            self.assertEqual(len(store.read("analysis_references")), 2)
            status = health.document(12)["sources"][
                "analysis_reference:isw_russian_offensive_campaign"
            ]
            self.assertEqual(status["status"], "partial")
            self.assertEqual(status["records"], 2)
            self.assertIn("scripted shard failure", status["error_message"])

    def test_analysis_family_cannot_enter_independent_reporting_count(self):
        config = Config(
            project={},
            hypotheses=[],
            indicators=[],
            news_sources=[],
            discovery_queries=[],
            claim_rules=[],
            analysis_sources=[self.source],
        )
        self.assertEqual(config.reporting_families, set())
        self.assertEqual(
            [error for error in validate_config(config) if error.startswith("analysis source")],
            [],
        )

    def test_tracker_and_diff_label_reference_as_non_evidence(self):
        config = Config(
            project={},
            hypotheses=[],
            indicators=[],
            news_sources=[],
            discovery_queries=[],
            claim_rules=[],
            analysis_sources=[self.source],
        )
        reference = {
            "title": "Russian Offensive Campaign Assessment, September 8, 2026",
            "url": (
                "https://understandingwar.org/research/russia-ukraine/"
                "russian-offensive-campaign-assessment-september-8-2026"
            ),
            "assessment_date": "2026-09-08",
            "sitemap_modified_at": "2026-09-09T03:06:45Z",
            "collected_at": "2026-09-09T07:00:00Z",
            "attribution": "Source: Institute for the Study of War",
            "rights_url": self.source.rights_url,
        }

        tracker = render_tracker(config, [], analysis_references=[reference])
        changes = render_changes(
            config,
            [],
            since="2026-09-09T00:00:00Z",
            analysis_references=[reference],
        )
        self.assertIn("## Analytical references", tracker)
        self.assertIn("not evidence records", tracker)
        self.assertIn("never counts as independent corroboration", tracker)
        self.assertIn("## New or modified analytical references", changes)
        self.assertIn("does not attest any claim", changes)


if __name__ == "__main__":
    unittest.main()
