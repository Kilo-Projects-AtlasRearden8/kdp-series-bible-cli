"""Tests for series bible data models."""

import pytest

from kdp_series_bible.models import (
    Character,
    Setting,
    TimelineEvent,
    SeriesBook,
    Bible,
    validate_model,
)
from kdp_series_bible.validator import ValidationError, validate_bible


def test_character_valid():
    char = Character(id="c1", name="Arya", role="protagonist", description="Brave.")
    assert validate_model(char) == []


def test_character_missing_required():
    char = Character(id="", name="")
    problems = validate_model(char)
    assert any("character id" in p for p in problems)
    assert any("character name" in p for p in problems)


def test_setting_valid():
    setting = Setting(id="s1", name="The Tavern", type="location", description="A dark tavern.")
    assert validate_model(setting) == []


def test_setting_missing_required():
    setting = Setting(id="", name="")
    problems = validate_model(setting)
    assert any("setting id" in p for p in problems)
    assert any("setting name" in p for p in problems)


def test_timeline_event_valid():
    event = TimelineEvent(id="t1", title="The Battle", date="Year 1", description="A big battle.")
    assert validate_model(event) == []


def test_timeline_event_missing_required():
    event = TimelineEvent(id="", title="")
    problems = validate_model(event)
    assert any("timeline event id" in p for p in problems)
    assert any("timeline event title" in p for p in problems)


def test_series_book_valid():
    book = SeriesBook(position=1, title="Book One", publication_date="2026-01-01")
    assert validate_model(book) == []


def test_series_book_invalid_position():
    book = SeriesBook(position=0, title="Book One")
    problems = validate_model(book)
    assert any("position" in p for p in problems)


def test_bible_to_dict_and_from_dict_roundtrip():
    bible = Bible(
        series_name="Test Series",
        series_order=[SeriesBook(position=1, title="One")],
        characters=[Character(id="c1", name="Hero")],
        settings=[Setting(id="s1", name="Village")],
        timeline=[TimelineEvent(id="t1", title="Start")],
    )
    data = bible.to_dict()
    assert data["series_name"] == "Test Series"
    assert len(data["characters"]) == 1
    restored = Bible.from_dict(data)
    assert restored.series_name == "Test Series"
    assert restored.characters[0].name == "Hero"
    assert restored.settings[0].name == "Village"
    assert restored.timeline[0].title == "Start"


def test_validate_bible_reports_problems():
    bible = Bible(series_name="", characters=[Character(id="", name="")])
    problems = validate_bible(bible)
    assert len(problems) > 0
    assert any("series_name" in p for p in problems)
