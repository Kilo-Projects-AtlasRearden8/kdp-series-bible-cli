# kdp-series-bible

Local-first CLI to build and maintain a KDP series bible: characters,
settings, timelines, and series order. Data is saved locally as JSON and can
be exported to Markdown. No network access, no API keys, no secrets.

Built by **Dylan Asdale** of **Asdale Dynamics, LLC** (Indiana, formed Oct
2026) — beginner-friendly AI education, books and guides, and practical tools
for authors and small businesses. Credit: Asdale Dynamics, LLC.

## Install

```bash
pip install .
```

or, for editable development:

```bash
pip install -e .
```

This provides the `kdp` command.

## Quick start

```bash
# Initialize a bible for your series
kdp init "The Massive AI Manual" --dir ./my_series_bible

# Add a character
kdp add-character c1 "Jordan Vale" --role protagonist --description "A nurse turned AI author." --dir ./my_series_bible

# Add a setting
kdp add-setting s1 "Asdale Dynamics HQ" --type location --description "Home office in Indiana." --dir ./my_series_bible

# Add a timeline event
kdp add-timeline-event t1 "Company formed" "Oct 2026" --related-characters c1 --related-settings s1 --dir ./my_series_bible

# Add a book to series order
kdp add-book 1 "The Massive AI Manual" --publication-date 2026 --dir ./my_series_bible

# List the bible
kdp list --dir ./my_series_bible

# Validate the data
kdp validate --dir ./my_series_bible

# Export to Markdown
kdp export-md series_bible.md --dir ./my_series_bible
```

## Commands

| Command | Purpose |
|---------|---------|
| `init NAME` | Create a new bible directory with a series name |
| `add-character ID NAME` | Add a character |
| `add-setting ID NAME` | Add a setting (place, world, object, organization) |
| `add-timeline-event ID TITLE DATE` | Add a dated timeline event |
| `add-book POSITION TITLE` | Add a book to series order |
| `list` | Summarize the bible |
| `validate` | Run data validation |
| `export-md [FILE]` | Export to Markdown (file or stdout) |

Use `--dir` to pick the bible storage directory (default: `.kdp_bible`).

## Data format

Each bible directory holds plain JSON files: `meta.json`, `characters.json`,
`settings.json`, `timeline.json`, `series_order.json`. Edit them by hand if
you like — `kdp validate` checks your work.

## Tests

```bash
pip install pytest
pytest
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
