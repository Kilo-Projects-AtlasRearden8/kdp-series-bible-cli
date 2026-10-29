"""Data models for the KDP series bible.

All models are plain dataclasses so they serialize cleanly to JSON and
Markdown. Validation lives in validator.py; this module defines shape only.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, asdict
from typing import Optional


@dataclass
class Character:
    """A person (or entity) in the series."""

    id: str
    name: str
    role: str = ""
    description: str = ""
    age: Optional[str] = None
    occupation: str = ""
    first_appearance: str = ""
    notes: str = ""

    def display_name(self) -> str:
        return self.name or self.id


@dataclass
class Setting:
    """A place or world element in the series."""

    id: str
    name: str
    type: str = ""  # e.g. location, world, organization, object
    description: str = ""
    first_appearance: str = ""
    notes: str = ""


@dataclass
class TimelineEvent:
    """A dated event in the series timeline."""

    id: str
    title: str
    date: str = ""  # free-form date string (keeps local-first simplicity)
    description: str = ""
    related_characters: list[str] = field(default_factory=list)
    related_settings: list[str] = field(default_factory=list)


@dataclass
class SeriesBook:
    """One book in the series, in order."""

    position: int
    title: str
    publication_date: str = ""
    asin: str = ""
    notes: str = ""


@dataclass
class Bible:
    """The complete series bible for one series."""

    series_name: str
    series_order: list[SeriesBook] = field(default_factory=list)
    characters: list[Character] = field(default_factory=list)
    settings: list[Setting] = field(default_factory=list)
    timeline: list[TimelineEvent] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "series_name": self.series_name,
            "series_order": [asdict(book) for book in self.series_order],
            "characters": [asdict(c) for c in self.characters],
            "settings": [asdict(s) for s in self.settings],
            "timeline": [asdict(t) for t in self.timeline],
        }

    @staticmethod
    def from_dict(data: dict) -> "Bible":
        def load(cls, items):
            return [cls(**item) for item in items]

        return Bible(
            series_name=data.get("series_name", ""),
            series_order=load(SeriesBook, data.get("series_order", [])),
            characters=load(Character, data.get("characters", [])),
            settings=load(Setting, data.get("settings", [])),
            timeline=load(TimelineEvent, data.get("timeline", [])),
        )


def validate_model(obj) -> list[str]:
    """Return a list of human-readable validation problems for one model."""
    from .validator import validate_character, validate_setting, validate_timeline_event, validate_series_book

    if isinstance(obj, Character):
        return validate_character(obj)
    if isinstance(obj, Setting):
        return validate_setting(obj)
    if isinstance(obj, TimelineEvent):
        return validate_timeline_event(obj)
    if isinstance(obj, SeriesBook):
        return validate_series_book(obj)
    return [f"unknown model type: {type(obj).__name__}"]
