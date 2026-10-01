# Repository layout and maintained sources

The `jev_learning` folder is the course root. The GitHub archive uses `jev-learning-course` as its
top-level folder. Keep the notebooks, helper files, and data together so imports remain portable.

```text
jev-learning-course/
├── README.md                 # GitHub landing page and lesson links
├── COURSE.md                 # Modules, outcomes, and checkpoints
├── 00_start_here.ipynb
├── ...                      # Ten notebooks, numbered 00–09
├── assignments/             # Three self-study assignments
├── data/                    # Fictional tickets and provenance
├── figures/                 # Saved figures used by lessons and README
├── .github/
│   ├── workflows/course.yml # Automated build, execution, and link checks
│   ├── ISSUE_TEMPLATE/      # Confusion, execution problem, and lesson idea
│   └── PULL_REQUEST_TEMPLATE.md
├── CONTRIBUTING.md
├── SETUP.md
├── SOURCES.md
├── requirements.txt
├── validate_course.py
├── package_course.py
├── ...                      # Generator and teaching-helper Python files
└── html/                    # Optional saved browser copies
```

## Where to edit

| Material | Maintained source |
|---|---|
| Lessons 01–05 | `build_notebooks.py`, `lesson_upgrades.py` |
| Public welcome, reader guides, recaps, and self-checks | `public_course.py` |
| Lessons 06–08 | `extra_lessons.py` |
| Lesson 09 | `related_lessons.py` |
| Local model and evaluation helpers | `lab_core.py` |
| Tables and plotting style | `tutorial_utils.py` |
| GitHub landing page and guides | Corresponding `.md` files |
| Printable practice and optional browser quiz | `practice_questions.py`, `build_practice.py` |
| Optional HTML exports and navigation | `build_site.py`, `public_site.py` |
| Course checks | `validate_course.py`, `package_course.py` |

`PRACTICE.md` is generated. Edit the question source to keep its two representations synchronized.
Other Markdown guides can be edited directly. See [CONTRIBUTING.md](CONTRIBUTING.md) for the rebuild flow.

## Generated and local files

Saved notebook outputs and published figures are included so GitHub readers can learn immediately.
The HTML copies are optional for local reading. GitHub's normal file view shows HTML source, so
the course's primary links use notebooks and Markdown.

`dist/` contains generated archives and package reports. `backups/` contains local snapshots.
Both are ignored by Git and excluded from the packaged course, along with environments and caches.
`qa_summary.json` records local QA and is not part of the public repository package.

[Course home](README.md) · [Publishing guide](GITHUB_PUBLISHING.md)
