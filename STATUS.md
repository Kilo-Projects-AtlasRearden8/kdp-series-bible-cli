# STATUS

## What was built

`kdp-series-bible` — a local-first Python CLI for building and maintaining a
KDP series bible: characters, settings, timelines, and series order.

- Data models: `Character`, `Setting`, `TimelineEvent`, `SeriesBook`, `Bible`
  (src/kdp_series_bible/models.py)
- JSON storage in a user-chosen bible directory (default `.kdp_bible`):
  meta.json, characters.json, settings.json, timeline.json, series_order.json
  (src/kdp_series_bible/storage.py)
- Markdown export: series order table + per-entity detail sections, with an
  Asdale Dynamics, LLC credit (src/kdp_series_bible/storage.py:
  `render_markdown`, `Storage.export_markdown`)
- Data validation: required fields, duplicate ids/positions, timeline
  cross-reference checks, all problems reported at once
  (src/kdp_series_bible/validator.py)
- CLI (`kdp`, argparse, stdlib only): init, add-character, add-setting,
  add-timeline-event, add-book, list, validate, export-md, version. `--dir`
  works anywhere in the command line.
  (src/kdp_series_bible/cli.py)
- Tests: 24 tests covering models, storage round-trips, Markdown export, and
  validation rules (tests/)
- No dependencies, no network, no API keys, no secrets, no personal data.
- MIT LICENSE, copyright line exactly:
  `Copyright (c) 2026 Asdale Dynamics, LLC`.
- README and STATUS.md credit Asdale Dynamics, LLC.
- Built for Dylan Asdale / Asdale Dynamics, LLC (Indiana, formed Oct 2026).

## How to run

```bash
pip install .                 # or pip install -e . for editable development
kdp init "My Series"          # creates .kdp_bible/
kdp add-character c1 "Name" --role protagonist --description "..."
kdp add-setting s1 "Place" --type location
kdp add-timeline-event t1 "Event" "Date"
kdp add-book 1 "Book One" --publication-date 2026
kdp list
kdp validate
kdp export-md bible.md
kdp --version
```

Use `--dir <path>` before or after the subcommand to choose a bible directory.

Tests:

```bash
pip install pytest
pytest
```

## Verification results

- `pip install .` builds and installs cleanly (setuptools, src layout).
- `pytest`: 24 passed, 0 failed.
- CLI smoke test: init + add character/setting/timeline event/book + list +
  validate + export-md all succeed; `--dir` works before and after the
  subcommand; `--version` works as both a global flag and a subcommand;
  Markdown output contains all sections and the Asdale Dynamics credit.
- Validation failure path returns exit code 1 and lists all problems found.
- `python -m kdp_series_bible --help` works.

## Known gaps

- Dates are free-form strings; no calendar parsing or sorting by date.
- Markdown table columns can misalign with very long cell text (cosmetic).
- No web UI, no import from other bible formats, no KDP/Amazon upload.
