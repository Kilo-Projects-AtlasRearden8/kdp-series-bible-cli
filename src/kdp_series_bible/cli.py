"""Command-line interface for the KDP series bible.

Pure stdlib (argparse). Local-first: everything lives on disk in the
chosen bible directory. No network, no keys, no secrets.
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .models import (
    Bible,
    Character,
    Setting,
    TimelineEvent,
    SeriesBook,
    validate_model,
)
from .storage import Storage, load_bible, save_bible, export_markdown
from .validator import validate_bible


def _storage_for(args) -> Storage:
    return Storage(args.dir)


def cmd_init(args) -> int:
    bible = Bible(series_name=args.name)
    storage = _storage_for(args)
    save_bible(bible, storage.directory)
    print(f"Initialized series bible '{args.name}' in {storage.directory}")
    return 0


def _add_entity(args, cls, bible_attr: str, constructor_fields) -> int:
    storage = _storage_for(args)
    bible = storage.load()
    data = {name: getattr(args, name) for name in constructor_fields}
    try:
        entity = cls(**data)
    except TypeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    problems = validate_model(entity)
    if problems:
        for problem in problems:
            print(f"Validation error: {problem}", file=sys.stderr)
        return 1
    getattr(bible, bible_attr).append(entity)
    save_bible(bible, storage.directory)
    print(f"Added {cls.__name__.lower()} '{getattr(args, constructor_fields[1] if len(constructor_fields) > 1 else constructor_fields[0])}'")
    return 0


def cmd_add_character(args) -> int:
    return _add_entity(
        args,
        Character,
        "characters",
        ("id", "name", "role", "description", "age", "occupation", "first_appearance", "notes"),
    )


def cmd_add_setting(args) -> int:
    return _add_entity(
        args,
        Setting,
        "settings",
        ("id", "name", "type", "description", "first_appearance", "notes"),
    )


def cmd_add_timeline_event(args) -> int:
    related_characters = [c.strip() for c in args.related_characters.split(",") if c.strip()] if args.related_characters else []
    related_settings = [c.strip() for c in args.related_settings.split(",") if c.strip()] if args.related_settings else []

    storage = _storage_for(args)
    bible = storage.load()
    try:
        event = TimelineEvent(
            id=args.id,
            title=args.title,
            date=args.date,
            description=args.description,
            related_characters=related_characters,
            related_settings=related_settings,
        )
    except TypeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    problems = validate_model(event)
    if problems:
        for problem in problems:
            print(f"Validation error: {problem}", file=sys.stderr)
        return 1
    bible.timeline.append(event)
    save_bible(bible, storage.directory)
    print(f"Added timeline event '{args.title}'")
    return 0


def cmd_add_book(args) -> int:
    storage = _storage_for(args)
    bible = storage.load()
    book = SeriesBook(
        position=args.position,
        title=args.title,
        publication_date=args.publication_date or "",
        asin=args.asin or "",
        notes=args.notes or "",
    )
    problems = validate_model(book)
    if problems:
        for problem in problems:
            print(f"Validation error: {problem}", file=sys.stderr)
        return 1
    bible.series_order.append(book)
    save_bible(bible, storage.directory)
    print(f"Added book #{args.position}: {args.title}")
    return 0


def cmd_list(args) -> int:
    storage = _storage_for(args)
    bible = storage.load()
    print(f"Series: {bible.series_name or '(untitled)'}")
    print(f"  directory: {storage.directory}")
    print(f"  books: {len(bible.series_order)}")
    print(f"  characters: {len(bible.characters)}")
    print(f"  settings: {len(bible.settings)}")
    print(f"  timeline events: {len(bible.timeline)}")
    if bible.series_order:
        print("\nSeries order:")
        for book in sorted(bible.series_order, key=lambda b: b.position):
            print(f"  #{book.position} {book.title} ({book.publication_date or 'unreleased'})")
    return 0


def cmd_validate(args) -> int:
    storage = _storage_for(args)
    bible = storage.load()
    problems = validate_bible(bible)
    if problems:
        print(f"Validation failed ({len(problems)} problem(s)):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("Bible is valid.")
    return 0


def cmd_export_md(args) -> int:
    storage = _storage_for(args)
    bible = storage.load()
    markdown = export_markdown(bible, args.output)
    if args.output:
        print(f"Exported Markdown to {args.output}")
    else:
        print(markdown)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kdp",
        description="Local-first CLI to build and maintain a KDP series bible.",
    )
    parser.add_argument(
        "--dir",
        default=".kdp_bible",
        help="Bible storage directory (default: .kdp_bible)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize a new series bible directory")
    p_init.add_argument("name", help="Name of the series")
    p_init.set_defaults(func=cmd_init)

    p_char = sub.add_parser("add-character", help="Add a character")
    p_char.add_argument("id", help="Character id")
    p_char.add_argument("name", help="Character name")
    p_char.add_argument("--role", default="")
    p_char.add_argument("--description", default="")
    p_char.add_argument("--age", default="")
    p_char.add_argument("--occupation", default="")
    p_char.add_argument("--first-appearance", default="")
    p_char.add_argument("--notes", default="")
    p_char.set_defaults(func=cmd_add_character)

    p_set = sub.add_parser("add-setting", help="Add a setting")
    p_set.add_argument("id", help="Setting id")
    p_set.add_argument("name", help="Setting name")
    p_set.add_argument("--type", default="")
    p_set.add_argument("--description", default="")
    p_set.add_argument("--first-appearance", default="")
    p_set.add_argument("--notes", default="")
    p_set.set_defaults(func=cmd_add_setting)

    p_tl = sub.add_parser("add-timeline-event", help="Add a timeline event")
    p_tl.add_argument("id", help="Event id")
    p_tl.add_argument("title", help="Event title")
    p_tl.add_argument("date", help="Event date (free-form)")
    p_tl.add_argument("--description", default="")
    p_tl.add_argument("--related-characters", default="", help="Comma-separated character ids")
    p_tl.add_argument("--related-settings", default="", help="Comma-separated setting ids")
    p_tl.set_defaults(func=cmd_add_timeline_event)

    p_book = sub.add_parser("add-book", help="Add a book to series order")
    p_book.add_argument("position", type=int, help="Position in series (1-based)")
    p_book.add_argument("title", help="Book title")
    p_book.add_argument("--publication-date", default="")
    p_book.add_argument("--asin", default="")
    p_book.add_argument("--notes", default="")
    p_book.set_defaults(func=cmd_add_book)

    sub.add_parser("list", help="Summarize the bible").set_defaults(func=cmd_list)
    sub.add_parser("validate", help="Validate the bible").set_defaults(func=cmd_validate)

    p_md = sub.add_parser("export-md", help="Export the bible to Markdown")
    p_md.add_argument("output", nargs="?", help="Output Markdown file (prints to stdout if omitted)")
    p_md.set_defaults(func=cmd_export_md)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
