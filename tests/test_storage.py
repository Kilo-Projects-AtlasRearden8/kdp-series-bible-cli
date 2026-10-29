"""Tests for JSON storage and Markdown export."""

import json
import os
import tempfile

from kdp_series_bible.models import (
    Bible,
    Character,
    Setting,
    TimelineEvent,
    SeriesBook,
)
from kdp_series_bible.storage import Storage, load_bible, save_bible, export_markdown


def _sample_bible() -> Bible:
    return Bible(
        series_name="Sample Series",
        series_order=[SeriesBook(position=1, title="First", publication_date="2026-01-01", asin="B000000000")],
        characters=[Character(id="c1", name="Hero", role="protagonist", description="The hero.")],
        settings=[Setting(id="s1", name="Village", type="location", description="A village.")],
        timeline=[TimelineEvent(id="t1", title="Start", date="Year 1", description="It began.")],
    )


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        bible = _sample_bible()
        save_bible(bible, tmp)
        loaded = load_bible(tmp)
        assert loaded.series_name == "Sample Series"
        assert len(loaded.characters) == 1
        assert loaded.characters[0].name == "Hero"
        assert len(loaded.series_order) == 1
        assert loaded.series_order[0].title == "First"
        assert len(loaded.timeline) == 1
        assert loaded.timeline[0].title == "Start"


def test_json_files_written():
    with tempfile.TemporaryDirectory() as tmp:
        save_bible(_sample_bible(), tmp)
        names = sorted(p.name for p in os.scandir(tmp))
        assert "meta.json" in names
        assert "characters.json" in names
        assert "settings.json" in names
        assert "timeline.json" in names
        assert "series_order.json" in names
        meta = json.loads(open(os.path.join(tmp, "meta.json")).read())
        assert meta["series_name"] == "Sample Series"


def test_load_missing_directory_returns_empty_bible():
    with tempfile.TemporaryDirectory() as tmp:
        empty_dir = os.path.join(tmp, "does_not_exist")
        bible = load_bible(empty_dir)
        assert bible.series_name == ""
        assert bible.characters == []


def test_export_markdown_contains_sections():
    markdown = export_markdown(_sample_bible())
    assert "# Sample Series — Series Bible" in markdown
    assert "## Series Order" in markdown
    assert "## Characters" in markdown
    assert "## Settings" in markdown
    assert "## Timeline" in markdown
    assert "First" in markdown
    assert "Hero" in markdown
    assert "Village" in markdown
    assert "Start" in markdown
    assert "Asdale Dynamics, LLC" in markdown


def test_export_markdown_writes_file():
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "bible.md")
        export_markdown(_sample_bible(), out)
        assert os.path.exists(out)
        content = open(out, encoding="utf-8").read()
        assert "# Sample Series — Series Bible" in content
