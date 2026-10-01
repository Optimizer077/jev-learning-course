# Read first, run when you are ready

## Option A: read without installation

1. Open [README.md](../README.md) in the GitHub repository.
2. Start with [00 · Start here](../notebooks/00_start_here.ipynb).
3. Follow the beginner path: 00 → 01 → 04. Saved explanations, results, and figures are included.

Use [COURSE.md](COURSE.md) for checkpoints and [PRACTICE.md](PRACTICE.md) for fold-open answers.
GitHub's notebook viewer is a reading view; it does not run Python cells.

### Optional browser version

Download and extract the whole course folder, then open `site/index.html` locally. GitHub displays
HTML files as source, so use the notebook and Markdown links when reading the repository online.

HTML lessons start in reading mode: explanations and saved results are visible, while Python code
is hidden. Select **Show Python code** at the top to inspect it. Browser pages do not execute Python.
The playground's sliders work in the browser and do not call any model.

Figures are embedded in the pages. Math typesetting uses a MathJax CDN and may need internet;
without it, equations may appear as LaTeX source. The home page and playground need no network.
The optional playground and interactive practice also work after downloading the complete folder.

## Option B: run in Google Colab

1. Choose a **Colab** link in [the lesson catalog](../notebooks/README.md).
2. Sign in to Google if Colab asks, and connect to a **CPU runtime**.
3. Choose **Runtime → Run all**. The first cell clones the public course repository
   to fetch the included helpers, fictional data, and artwork. No Jev key is requested.
4. Read the outputs, change one value, and run the affected cell again.
5. Save a copy to your own Drive if you want to keep edits. A new runtime may discard local files.

Colab needs internet for the initial clone. NumPy, Matplotlib, and IPython are the notebook
dependencies; if a runtime reports a missing package, run `%pip install numpy matplotlib ipython`
in a new cell, then restart and run the lesson. No GPU or model download is necessary.
The optional live API stays disabled in lesson 05.
Teaching diagrams are embedded in saved notebook outputs. They remain visible when you open
a single notebook; rerunning them loads the accompanying PNGs from the cloned course.

## Option C: run and change the examples locally

You need Python and internet access once to install packages. Python 3.11 or newer is recommended;
the delivered notebooks were executed with **Python 3.13.13 on Windows**. The GitHub workflow
also checks the course on Ubuntu with Python 3.13. macOS execution has not been tested.
No GPU or API key is needed.

### Windows (PowerShell)

Open PowerShell **inside the extracted course folder**, where `requirements.txt` is located.
In File Explorer, open the folder, type `powershell` in the address bar, and press Enter.
Run these commands one at a time:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyter lab
```

If `python` is not found, install Python from [python.org](https://www.python.org/downloads/),
enable its PATH option, and reopen PowerShell. If available, `py` can replace `python` in the
first two commands. These instructions do not require activating the environment.

### macOS or Linux (Terminal)

Open Terminal in the extracted course folder. Run:

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m jupyter lab
```

Some Linux distributions provide `venv` separately; follow your distribution's instructions if
Python reports that virtual-environment support is missing.

### Your first run

1. JupyterLab opens in your browser. Open `notebooks/00_start_here.ipynb`.
2. Select the Python kernel from this environment if prompted.
3. Choose **Kernel → Restart Kernel and Run All Cells**. Confirm the restart if asked.
4. Wait for the kernel to become idle. The routing example should print `technical`.
5. Open lesson 01. Read its introduction, predict each result, then run a cell with **Shift+Enter**.

A **cell** is one block of text or code; a **kernel** is the Python process holding your variables.
Restarting clears those variables. Running top to bottom recreates them. Use Run All after edits
if a result seems inconsistent.

VS Code also works: install its Python and Jupyter extensions, open the whole folder, and choose
`.venv` as the notebook kernel. Preserve the `notebooks/`, `src/`, `data/`, and `assets/` folders.

## Common problems

| Symptom | Try this |
|---|---|
| `No module named numpy` or another package | Run the install command; choose that same `.venv` as your kernel. |
| `No module named tutorial_utils` / `lab_core` | Keep `src/` in the course folder and run the first setup cell. In Colab, check that the clone completed. |
| Colab says the cached course is incomplete | Start a fresh Colab runtime and run all again. The setup will fetch a complete course; it does not overwrite the partial folder. |
| `FileNotFoundError` for tickets | Keep `data/tickets.json` in the course folder; preserve the original folder structure. |
| A variable is not defined | Restart the kernel and run every cell in order. |
| HTML shows old output after an edit | HTML is a saved copy. Read current output in Jupyter or rebuild using the maintainer guide. |
| An equation shows dollar signs or LaTeX | Allow MathJax to load, or read the surrounding plain-language explanation. |
| A check fails after an experiment | Checks may describe original parameters. Undo the change or update the expected result deliberately. |
| The optional API fails | Local lessons still work. Check lesson 05 and the provider's current docs. |

## Optional: real Jev

Leave `RUN_LIVE = False` in lesson 05 to inspect the request without a key. To call the service,
use your own TypeSafe account, set the flag to `True`, and provide your key through the hidden prompt
or `TYPESAFE_API_KEY` environment variable. Usage may be billed. Do not save a key in code or output.
The delivered outputs contain no live Jev results.

[Course home](../README.md) · [FAQ](FAQ.md)
