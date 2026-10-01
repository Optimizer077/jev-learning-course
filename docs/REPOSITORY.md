# Repository layout

[Course home](../README.md) · [Contributing](CONTRIBUTING.md) · [Setup](SETUP.md)

The root contains the course README, requirements, and repository configuration.
Learners can start without browsing the implementation files.

```text
jev-learning-course/
├── README.md           Course landing page
├── requirements.txt    Local Python dependencies
├── notebooks/          Ten lessons and their Colab links
├── docs/               Curriculum, references, and maintainer guides
├── assignments/        Three self-study tasks
├── data/               Authored tickets and provenance
├── assets/             Course graphics and exported figures
├── src/                Local teaching models and plotting helpers
├── scripts/            Build, execute, validate, and package tools
├── site/               Optional offline HTML copies and playground
└── .github/            Course checks and feedback templates
```

## Maintained sources

| Material | Edit here |
|---|---|
| Base lessons 01–05 | `scripts/build_notebooks.py` |
| Extensions and guided explanations | `scripts/lesson_upgrades.py`, `scripts/public_course.py` |
| Lessons 00 and 06–08 | `scripts/extra_lessons.py` |
| Lesson 09 | `scripts/related_lessons.py` |
| Course links and notebook environment setup | `scripts/course_paths.py` |
| Numerical models and data loading | `src/lab_core.py` |
| Notebook figures and table style | `src/tutorial_utils.py` |
| Header and learning-path artwork | `scripts/build_visuals.py` |
| Practice questions | `scripts/practice_questions.py` |
| Optional HTML exports | `scripts/build_site.py`, `scripts/public_site.py`, `scripts/build_practice.py` |

Keep the whole repository together. A notebook finds `src/` from its course folder;
Colab fetches the public repository when the companion files are missing.

## Generated files

The executed notebooks, SVG artwork, figure images, optional `site/` exports,
`validation.json`, and `requirements-tested.txt` are committed for readers.
The build scripts regenerate them. Standalone Markdown guides are maintained directly;
`PRACTICE.md` is generated from the question bank.

`dist/`, `backups/`, environments, and execution caches stay local and are ignored by Git.
They are excluded from the public archives. See [sharing](SHARING.md) for the rebuild commands.
