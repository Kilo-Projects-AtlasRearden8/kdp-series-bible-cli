"""KDP series bible package: characters, settings, timelines, series order."""

from .models import (
    Character,
    SeriesBook,
    Setting,
    TimelineEvent,
    Bible,
    validate_model,
)
from .storage import Storage, load_bible, save_bible
from .validator import validate_bible, ValidationError

__all__ = [
    "Character",
    "SeriesBook",
    "Setting",
    "TimelineEvent",
    "Bible",
    "validate_model",
    "Storage",
    "load_bible",
    "save_bible",
    "validate_bible",
    "ValidationError",
]

__version__ = "0.1.0"
