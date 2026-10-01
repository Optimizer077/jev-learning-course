# Maintainer guide: edit, rebuild, and share

## Share the complete course

Run `python package_course.py` with the requirements installed. It checks notebook outputs and
local HTML links, then creates `dist/jev-learning-public.zip` and `dist/jev-learning-github.zip`.
The public archive uses a `jev-learning` folder; the GitHub archive uses `jev-learning-course`.
Both contain the complete course. The README is the starting point for GitHub readers.

It includes lessons, saved results, browser pages, Python helpers, references, and fictional data.
It excludes local backups, caches, environments, and earlier packaging output. You can upload the
extracted public folder to your repository or static host. The script does not publish anything.

For the GitHub repository layout and publishing commands, see [GITHUB_PUBLISHING.md](GITHUB_PUBLISHING.md).

Before publishing under a reuse license, choose your author attribution and license; neither is
invented on your behalf. Keep the independent-course notice and source links.

## Edit the course

For personal study, edit the notebooks. For maintained editions, edit their source:

| File | Purpose |
|---|---|
| `build_notebooks.py` | Original lessons 01–05 and notebook generation |
| `lesson_upgrades.py` | Additional experiments for lessons 01–05 |
| `extra_lessons.py` | Lessons 06–08; original 00 scaffold |
| `related_lessons.py` | Optional lesson 09: local rules, lexical prototypes, and a learned classifier |
| `public_course.py` | Public welcome lesson, reader guides, recaps, and self-checks |
| `lab_core.py` | NumPy teaching model and evaluation functions |
| `tutorial_utils.py` | Plot and table helpers |
| `build_site.py` / `public_site.py` | Browser pages, reading mode, and navigation |
| `build_practice.py` / `practice_questions.py` | Guided browser practice and printable companion |
| `data/tickets.json` | Fictional text-routing dataset with fixed splits |

Back up personal notebook edits before regeneration: `build_notebooks.py` recreates cells and
clears saved output. The source files are the maintained version of the course.

## Rebuild a public edition

Use the Python executable from your course environment. Replace `python` below with
`.\.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on macOS/Linux.

```bash
python build_notebooks.py
python execute_notebooks.py
python validate_course.py
python package_course.py
```

The executor runs each notebook in a fresh kernel, saves results, and rebuilds HTML.
The optional API flag stays off by default. `validation.json` records execution;
`requirements-tested.txt` records exact package versions. `python build_site.py` rebuilds only
the home, playground, and support pages; lesson exports require the executor.

Before sharing an edited edition, read its HTML, try its playground, and check explanations
against displayed results. Recheck official API claims against current documentation.
Keep teaching examples labeled; tiny local experiments are not provider benchmarks.

`PRACTICE.md` is generated from `practice_questions.py` when the site is built. Edit the question
source to keep interactive and printable practice synchronized. `LEARNING_GUIDE.md` can be edited directly.

[Course home](README.md) · [Reader setup](SETUP.md)
