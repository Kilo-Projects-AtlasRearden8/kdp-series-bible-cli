"""Tests for data validation rules."""

from kdp_series_bible.models import (
    Character,
    Setting,
    TimelineEvent,
    SeriesBook,
    Bible,
)
from kdp_series_bible.validator import (
    validate_character,
    validate_setting,
    validate_timeline_event,
    validate_series_book,
    validate_bible,
    ValidationError,
)


def test_validate_character_empty_problems_when_valid():
    assert validate_character(Character(id="c1", name="Hero")) == []


def test_validate_character_missing_name():
    problems = validate_character(Character(id="c1", name=""))
    assert any("character name" in p for p in problems)


def test_validate_setting_missing_id():
    problems = validate_setting(Setting(id="", name="Village"))
    assert any("setting id" in p for p in problems)


def test_validate_timeline_event_missing_title():
    problems = validate_timeline_event(TimelineEvent(id="t1", title=""))
    assert any("timeline event title" in p for p in problems)


def test_validate_series_book_bad_position():
    problems = validate_series_book(SeriesBook(position=-1, title="X"))
    assert any("position" in p for p in problems)


def test_validate_bible_duplicate_ids():
    bible = Bible(
        series_name="S",
        characters=[Character(id="c1", name="A"), Character(id="c1", name="B")],
    )
    problems = validate_bible(bible)
    assert any("duplicate character id" in p for p in problems)


def test_validate_bible_unknown_timeline_reference():
    bible = Bible(
        series_name="S",
        timeline=[TimelineEvent(id="t1", title="E", related_characters=["nope"])],
    )
    problems = validate_bible(bible)
    assert any("unknown character" in p for p in problems)


def test_validate_bible_all_valid():
    bible = Bible(
        series_name="S",
        series_order=[SeriesBook(position=1, title="One")],
        characters=[Character(id="c1", name="A")],
        settings=[Setting(id="s1", name="B")],
        timeline=[TimelineEvent(id="t1", title="E", related_characters=["c1"], related_settings=["s1"])],
    )
    assert validate_bible(bible) == []


def test_validation_error_is_exception():
    assert issubclass(ValidationError, Exception)
