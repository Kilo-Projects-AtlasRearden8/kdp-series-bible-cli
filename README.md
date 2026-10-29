# kdp-series-bible

A friendly, local-first command-line tool for building and maintaining a KDP
series bible: your characters, settings, timelines, and series order, all saved
locally as JSON and exportable to Markdown.

Built by **Dylan Asdale** — a registered nurse turned AI author — and
**Asdale Dynamics, LLC** (Indiana, formed October 2026). Asdale Dynamics makes
beginner-friendly AI education, books and guides, and practical tools for
authors and small businesses. Credit: Asdale Dynamics, LLC.

This tool is written in plain Python with no dependencies, no network access,
no API keys, and no secrets. Your data stays on your computer.

## Who this is for

If you're writing a series (KDP or otherwise) and you want a simple place to
keep track of who your characters are, where your story happens, when things
occur, and what order your books go in — this is for you. No account required,
no cloud, no subscription.

## Install

```bash
pip install .
```

For editable development:

```bash
pip install -e .
```

This gives you the `kdp` command.

## Quick start

```bash
# 1. Create a bible for your series
kdp init "The Massive AI Manual"

# 2. Add a character
kdp add-character c1 "Jordan Vale" --role protagonist \
  --description "A nurse turned AI author." --age 34 --occupation "RN"

# 3. Add a setting
kdp add-setting s1 "Asdale Dynamics HQ" --type location \
  --description "Home office in Indiana."

# 4. Add a timeline event
kdp add-timeline-event t1 "Company formed" "Oct 2026" \
  --related-characters c1 --related-settings s1

# 5. Add a book to your series order
kdp add-book 1 "The Massive AI Manual" --publication-date 2026

# 6. See your bible
kdp list

# 7. Check your data for problems
kdp validate

# 8. Export a Markdown bible you can read or print
kdp export-md series_bible.md
```

By default, everything lives in a `.kdp_bible` folder in your current
directory. Use `--dir` to put it somewhere else:

```bash
kdp init "My Series" --dir ./my_series_bible
kdp --dir ./my_series_bible list
kdp validate --dir ./my_series_bible
```

`--dir` works wherever you put it — before or after the subcommand.

## Commands

| Command | What it does |
|---------|--------------|
| `init NAME` | Create a new series bible with a series name |
| `add-character ID NAME` | Add a character |
| `add-setting ID NAME` | Add a setting (place, world, object, organization) |
| `add-timeline-event ID TITLE DATE` | Add a dated event in your timeline |
| `add-book POSITION TITLE` | Add a book to your series order |
| `list` | Summarize your bible |
| `validate` | Check your data for problems |
| `export-md [FILE]` | Export to Markdown (file, or print to screen) |
| `version` | Show the version |

Each command also accepts `--help` for details.

## Data format

Your bible folder holds plain JSON files you can open and edit by hand:

- `meta.json` — your series name
- `characters.json` — your characters
- `settings.json` — your settings
- `timeline.json` — your timeline events
- `series_order.json` — your books in order

Run `kdp validate` after editing by hand to make sure everything still checks
out.

## Markdown export

`kdp export-md series_bible.md` writes a readable Markdown bible with tables
for your series order, characters, settings, and timeline, plus detail
sections for each one. It includes a credit to Asdale Dynamics, LLC.

## Tests

```bash
pip install pytest
pytest
```

There are 24 tests covering models, storage round-trips, Markdown export, and
data validation rules.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC (Indiana, formed October 2026) is the company of Dylan
Asdale, registered nurse and AI author. The LLC focuses on beginner-friendly
AI education, books and guides, and practical tools — including open-source
apps and templates for authors and small businesses. Dylan's book *The Massive
AI Manual* and hub site dylanasdale.github.io explain AI "like a friend
would": plain English, step by step, never condescending.

This tool is part of that mission: practical, local-first software authors can
actually use, with nothing hidden and nothing phoning home.
