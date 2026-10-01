# Contributing to the course

Thank you for helping a learner understand an idea, reproduce an experiment, or find a mistake.
Small, focused changes are easiest to review.

## Report a problem

Use the repository's issue templates. Include the lesson or guide, the step that caused confusion,
what you expected, and what you observed. For an execution problem, include your Python version,
operating system, and the relevant error text. For a teaching problem, explain the interpretation
that led you astray.

## Propose a change

1. Describe the learner's problem and the resulting improvement.
2. Edit the maintained source listed in [REPOSITORY.md](REPOSITORY.md), or the relevant Markdown guide.
3. Keep the lesson's prerequisites and main question clear. Mark deeper material as optional.
4. Link factual Jev claims to primary provider documentation. Label local examples and generic mechanisms.
5. Rebuild the affected material, check saved outputs, and verify local links.
6. Describe your validation and any remaining gap in the pull request.

Notebook generation recreates cells. For course contributions, edit the generator source and
regenerate notebooks; use direct notebook edits for personal experiments. Avoid committing a
virtual environment, local backups, or a changed API key. The supplied live API flag stays false.

## Local checks

Install the course requirements using [SETUP.md](SETUP.md), then run:

```bash
python validate_course.py
```

For a maintained lesson change, run:

```bash
python build_notebooks.py
python execute_notebooks.py
python validate_course.py
python package_course.py
```

Use the Python executable from your course environment. Regeneration clears notebook outputs;
execution recreates the saved results. Back up your personal notebook edits first.

`validate_course.py` checks saved notebook execution, packaged files, local HTML references,
and Markdown/notebook links. It does not access external websites. The GitHub workflow also
rebuilds and executes the maintained lesson source in fresh kernels.

## Teaching standards

- Explain the idea in words before introducing the equation or implementation.
- Ask learners to predict a change, then explain the observation.
- Keep data splits and evaluation denominators visible.
- Inspect failure cases alongside aggregate results.
- Preserve the distinction between type validity, accuracy, calibration, and permissions.
- Keep similarity scores distinct from probabilities and provider confidence fields.
- Avoid benchmark claims that the supplied experiments do not establish.

For a documentation-only change, link validation is usually sufficient. For a computation change,
execute the affected lesson and inspect its saved figures and conclusions. Before a public edition,
run the complete course and package check.

[Course home](README.md) · [Maintainer guide](SHARING.md)
