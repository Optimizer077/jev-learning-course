# Prepare and publish the GitHub course

## Use the course archive as the repository root

Run `python package_course.py` to create:

- `dist/jev-learning-github.zip`: a `jev-learning-course` folder with the README, ten notebooks,
  guides, assignments, data, helper code, and `.github` configuration.
- `dist/jev-learning-public.zip`: the same complete course under `jev-learning`, suitable for direct sharing.

Extract the GitHub archive into a new folder. Publish that extracted course folder as the repository
root. The unrelated projects from the surrounding workspace are not included.

Suggested repository name: **`jev-learning-course`**.

Suggested description:

> A self-paced notebook course on Jev, typed AI decisions, calibration, and related models.

Suggested topics: `jev`, `typesafe-ai`, `machine-learning`, `jupyter-notebook`, `calibration`, `education`.

## Add your repository information

Choose the repository owner, visibility, and author attribution. The supplied course does not
invent an owner URL or license. Select and add the license you intend to use before presenting
the material under that license.

Keep the source links, data provenance, and independent-course notice. A current maintainer can
update the documentation-check date after rechecking provider claims.

## Publish using Git

Create an empty GitHub repository under your account. Then open a terminal in the **extracted
course folder** and run:

```bash
git init
git add .
git commit -m "Add Jev learning course"
git branch -M main
git remote add origin "PASTE_YOUR_REPOSITORY_URL_HERE"
git push -u origin main
```

Replace the quoted placeholder with the real remote URL from your repository. These are publishing
instructions, not commands run by the course's build scripts.

## Check the first publication

- The README appears at the repository root, with the lesson-00 link near the top.
- Notebook links, Markdown guides, assignment links, and the README figure resolve.
- The course workflow finishes successfully; it produces a checked ZIP as a workflow artifact.
- New issues offer the confusion, execution-problem, and lesson-idea templates.

The workflow uses Python 3.13 on Ubuntu. The delivered local run was on Windows; a successful
GitHub run will provide the separate hosted validation. The workflow performs checks and creates
an artifact; it does not publish a website or call the live Jev API under the supplied defaults.

For later updates, edit the maintained sources and follow [CONTRIBUTING.md](CONTRIBUTING.md).

[Course home](README.md) · [Repository layout](REPOSITORY.md)
