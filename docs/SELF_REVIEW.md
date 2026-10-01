# Self-review and repairs

Reviewed on **2026-10-02** for a beginner reading on GitHub, a learner running in Colab,
and a contributor rebuilding the course. [Course home](../README.md) · [Visual guide](VISUAL_GUIDE.md)

## What the review found

| Finding | Repair |
|---|---|
| The banner skipped the focused question and criteria. | The header now names them; a four-step ticket diagram traces evidence, question, estimate, and action. |
| The horizontal path graphic became too small on a phone. | Added stacked mobile graphics, stronger text contrast, and explicit prerequisites for the coding paths. |
| The first checkpoint included calibration before its lesson. | Module 1 uses questions 1–6; workflow uses 7; calibration and costs use 8–9; the project uses 10–12. |
| The illustrative Choice distribution differed between the opening examples. | The basic example now consistently uses 90% technical, 6% billing, and 4% other. These remain invented probabilities. |
| The FAQ omitted Colab's download and sign-in requirements. | Updated the FAQ and retained a separate local, offline reading path. |
| A partial Colab cache could produce a confusing clone failure. | Check for all required companions, reuse a complete cache, and explain how to recover from an incomplete one. |
| Responsive image sources were outside the link checks. | Validate and rewrite `srcset` references alongside ordinary image and page links. |
| GitHub checks used actions with a deprecated Node runtime. | Updated the three actions to current releases checked through the official repositories. |

## What was checked

- Notebook format and execution in fresh kernels.
- Local Markdown, notebook, HTML, and responsive-image links in the packaged course.
- Colab lesson destinations and a local simulation of fresh download, cached reuse, and incomplete-cache recovery.
- The exported SVGs and local raster previews, including the new mobile artwork, labels, values, and clipping. Track-label text has contrast of at least 4.5:1 against its card background.
- GitHub's Markdown renderer preserves both responsive picture elements; the mobile artwork was inspected at 360 pixels wide.
- Worked figures against their inputs: Choice sums to 1; Score is 1.65; eight yes outcomes out of ten give 80%.
- The repository still has five files at the root; backups, credentials, environments, and build output stay out of Git.

Execution records are in [validation.json](validation.json). The
[GitHub workflow](https://github.com/Optimizer077/jev-learning-course/actions/workflows/course.yml)
records the separate Ubuntu checks and produces a checked archive.

## Limits of this review

No webpages or hosted Colab runtimes were opened. The SVG artwork was inspected through local
raster previews; browser layout and GitHub's image switching were not visually previewed.
Local Colab simulation checks setup behavior, not Google's authentication or runtime availability.
No live Jev call was made. The 54 authored messages remain a teaching dataset, not a benchmark.

The review does not verify unpublished Jev internals or establish production reliability.
Provider descriptions retain the source-check date in [SOURCES.md](SOURCES.md).

Action release sources: [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1),
[setup-python v7.0.0](https://github.com/actions/setup-python/releases/tag/v7.0.0), and
[upload-artifact v7.0.1](https://github.com/actions/upload-artifact/releases/tag/v7.0.1).
