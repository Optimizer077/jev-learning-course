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

## Second pass: project clarity and portable visuals

| Finding | Repair |
|---|---|
| The curriculum checkpoint was fixed, but the short study plan still introduced calibration too early. | Aligned both: questions 1–6 after basics, 7 after workflows, 8–9 after calibration and costs, 10–12 after the project. |
| The switch from introductory queue options to project labels was easy to miss. | Explicitly explain the new billing/technical/account question and the out-of-domain `other` stress label. |
| Data-split roles and word-order failure relied mostly on prose and tables. | Added two diagrams beside the project steps and in the visual guide, with predict-and-explain checks. |
| Relative SVG links relied on companion files being resolved by a notebook viewer. | Embedded PNG artwork in saved outputs; the first Colab cell also fetches and checks the companion PNGs for rerunning. |
| The two failure labs repeated the same authored pair independently. | Both labs and the diagram use a single pair definition; the visual reads the actual training vocabulary. |
| The HTML exporter replaced useful image descriptions with a generic heading. | Preserve authored image descriptions; use the heading fallback only for unlabelled figures. |
| Section links did not match exported heading IDs; some IDs also retained literal URL escapes. | Normalize section IDs in course exports, update their anchors and outlines, and check every local HTML section destination. |

The new data counts were reconciled against all JSON rows. The word-order diagram was checked
against both full token sets and the actual training-only vocabulary: `failed` is unseen, and
the same four features are active in both messages. Adding that unseen word would still leave
their word-presence vectors identical.

The new diagrams were inspected as local raster previews, including 360-pixel color and grayscale views. The saved
notebook outputs, image descriptions, Colab setup simulation, rebuilt exports, and archive links
were checked again. Notebook execution records remain in [validation.json](validation.json).
The browser and hosted-Colab limits described above still apply.
