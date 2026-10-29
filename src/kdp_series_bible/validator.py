"""Validation rules for series bible models.

Pure functions: take a model, return a list of problem strings. Empty list
means valid. No network, no keys, no secrets.
"""

from __future__ import annotations

from .models import Character, Setting, TimelineEvent, SeriesBook


class ValidationError(Exception):
    """Raised when a bible fails validation and the caller wants an exception."""


def _required(value, field_name: str) -> list[str]:
    if not str(value).strip():
        return [f"{field_name} is required"]
    return []


def validate_character(char: Character) -> list[str]:
    problems = _required(char.id, "character id")
    problems += _required(char.name, "character name")
    if char.role and len(char.role) > 60:
        problems.append("character role is too long (max 60 chars)")
    if char.age is not None and len(str(char.age)) > 10:
        problems.append("character age is too long")
    return problems


def validate_setting(setting: Setting) -> list[str]:
    problems = _required(setting.id, "setting id")
    problems += _required(setting.name, "setting name")
    return problems


def validate_timeline_event(event: TimelineEvent) -> list[str]:
    problems = _required(event.id, "timeline event id")
    problems += _required(event.title, "timeline event title")
    return problems


def validate_series_book(book: SeriesBook) -> list[str]:
    problems = _required(book.title, "series book title")
    if not isinstance(book.position, int) or book.position < 1:
        problems.append("series book position must be a positive integer")
    return problems


def validate_bible(bible) -> list[str]:
    """Validate every model in a Bible. Returns all problems found."""
    problems: list[str] = []
    if not str(bible.series_name).strip():
        problems.append("bible series_name is required")

    seen_ids: dict[str, set[str]] = {
        "character": set(),
        "setting": set(),
        "timeline": set(),
        "series_book": set(),
    }

    for char in bible.characters:
        problems += [f"character '{char.name}': {p}" for p in validate_character(char)]
        if char.id in seen_ids["character"]:
            problems.append(f"duplicate character id: {char.id}")
        seen_ids["character"].add(char.id)

    for setting in bible.settings:
        problems += [f"setting '{setting.name}': {p}" for p in validate_setting(setting)]
        if setting.id in seen_ids["setting"]:
            problems.append(f"duplicate setting id: {setting.id}")
        seen_ids["setting"].add(setting.id)

    for event in bible.timeline:
        problems += [f"timeline event '{event.title}': {p}" for p in validate_timeline_event(event)]
        if event.id in seen_ids["timeline"]:
            problems.append(f"duplicate timeline event id: {event.id}")
        seen_ids["timeline"].add(event.id)

    for book in bible.series_order:
        problems += [f"book #{book.position} '{book.title}': {p}" for p in validate_series_book(book)]
        if book.position in seen_ids["series_book"]:
            problems.append(f"duplicate series book position: {book.position}")
        seen_ids["series_book"].add(book.position)

    # Cross-references: timeline events should reference known ids.
    known_characters = {c.id for c in bible.characters}
    known_settings = {s.id for s in bible.settings}
    for event in bible.timeline:
        for ref in event.related_characters:
            if ref not in known_characters:
                problems.append(
                    f"timeline event '{event.title}' references unknown character: {ref}"
                )
        for ref in event.related_settings:
            if ref not in known_settings:
                problems.append(
                    f"timeline event '{event.title}' references unknown setting: {ref}"
                )

    return problems
