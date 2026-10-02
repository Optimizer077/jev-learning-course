"""Shared course paths and links; independent of the command's working directory."""
import os
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / 'notebooks'
DOCS = ROOT / 'docs'
SITE = ROOT / 'site'
EXPORTS = SITE / 'lessons'
NOTEBOOK_COUNT = 11


def html_references(tag):
    """Read ordinary image/link URLs and responsive picture sources."""
    for attribute in ('href', 'src'):
        if tag.has_attr(attribute):
            yield tag[attribute]
    if tag.has_attr('srcset') and not tag['srcset'].startswith('data:'):
        for candidate in tag['srcset'].split(','):
            if candidate.strip():
                yield candidate.strip().split()[0]


def legacy_location(name):
    """Resolve the original flat authoring links into the organized layout."""
    path = Path(name)
    if path.parent == Path('.'):
        if path.suffix == '.md' and name != 'README.md':
            return 'docs/' + name
        if path.suffix == '.ipynb':
            return 'notebooks/' + name
        if path.suffix == '.html':
            return 'site/' + name
    if name.startswith('figures/'):
        return 'assets/' + name
    if name.startswith('html/'):
        return 'site/lessons/' + name[5:]
    return name


def rewrite_legacy_markdown(source, destination):
    """Keep authored lesson links readable while exporting to their real folder."""
    parent = (ROOT / destination).parent

    def rewrite(match):
        link = urlsplit(match.group(2))
        if link.scheme or link.netloc or not link.path:
            return match.group(0)
        target = ROOT / legacy_location(unquote(link.path))
        relative = Path(os.path.relpath(target, parent)).as_posix()
        return match.group(1) + urlunsplit(('', '', relative, link.query, link.fragment)) + match.group(3)

    return re.sub(r'(\]\()([^\s)]+)(\))', rewrite, source)


NOTEBOOK_SETUP = '''# Find the included teaching helpers from the course folder.
from pathlib import Path
import sys
REQUIRED_FILES = ("src/lab_core.py", "src/tutorial_utils.py", "src/torch_lab.py",
                  "data/tickets.json", "data/torch_toy.json",
                  "assets/decision-flow.png", "assets/question-types.png",
                  "assets/calibration-counts.png", "assets/data-splits.png", "assets/word-order.png")
COURSE_ROOT = next((p for p in (Path.cwd(), *Path.cwd().parents)
                    if all((p / name).is_file() for name in REQUIRED_FILES)), None)
# Colab opens a single notebook; fetch its companion code and fictional data.
if COURSE_ROOT is None:
    try:
        import google.colab
    except ImportError:
        pass
    else:
        import subprocess
        COURSE_ROOT = Path("/content/jev-learning-course")
        if COURSE_ROOT.exists() and not all((COURSE_ROOT / name).is_file() for name in REQUIRED_FILES):
            raise FileNotFoundError("The cached Colab course is incomplete. Start a fresh runtime and run all again.")
        if not COURSE_ROOT.exists():
            subprocess.run(["git", "clone", "--depth", "1",
                            "https://github.com/Optimizer077/jev-learning-course.git",
                            str(COURSE_ROOT)], check=True)
if COURSE_ROOT is None:
    raise FileNotFoundError("Extract the complete course and open it from its folder.")
if str(COURSE_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT / "src"))
'''
