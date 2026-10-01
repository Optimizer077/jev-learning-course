"""Validate and zip the public course using an explicit file allowlist. Never uploads."""
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

import nbformat
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
ROOT_FILES = [
    'README.md', 'COURSE.md', 'CONTRIBUTING.md', 'REPOSITORY.md', 'GITHUB_PUBLISHING.md',
    'SETUP.md', 'FAQ.md', 'SHARING.md', 'GLOSSARY.md', 'SOURCES.md', 'LEARNING_GUIDE.md', 'PRACTICE.md', 'MODEL_GUIDE.md', 'QUICK_REFERENCE.md',
    'requirements.txt', 'requirements-tested.txt', 'validation.json', '.gitignore',
    'index.html', 'playground.html', 'practice.html', 'build_practice.py', 'practice_questions.py', 'build_notebooks.py', 'lesson_upgrades.py',
    'extra_lessons.py', 'related_lessons.py', 'public_course.py', 'lab_core.py', 'tutorial_utils.py',
    'execute_notebooks.py', 'build_site.py', 'public_site.py', 'package_course.py', 'validate_course.py',
    'data/README.md', 'data/tickets.json',
    '.gitattributes', '.editorconfig',
    '.github/workflows/course.yml', '.github/PULL_REQUEST_TEMPLATE.md',
    '.github/ISSUE_TEMPLATE/config.yml', '.github/ISSUE_TEMPLATE/learning_question.md',
    '.github/ISSUE_TEMPLATE/execution_problem.md', '.github/ISSUE_TEMPLATE/lesson_idea.md',
    'assignments/README.md', 'assignments/01_design_a_decision.md',
    'assignments/02_probabilities_and_actions.md', 'assignments/03_evaluate_a_router.md',
]


def public_files(root=ROOT):
    files = [root/name for name in ROOT_FILES]
    files += sorted(root.glob('[0-9][0-9]_*.ipynb'))
    files += sorted((root/'html').glob('*.html'))
    files += sorted((root/'figures').glob('*.png'))
    missing = [str(p.relative_to(root)) for p in files if not p.is_file()]
    if missing:
        raise ValueError(f'Missing course files: {missing}. Build and execute the course first.')
    return sorted(set(files))


def validate(root=ROOT):
    files = public_files(root)
    included = {p.resolve() for p in files}
    notebooks = sorted(root.glob('[0-9][0-9]_*.ipynb'))
    if len(notebooks) != 10:
        raise ValueError(f'Expected ten lessons, found {len(notebooks)}.')
    code_cells = figures = 0
    for path in notebooks:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        for cell in nb.cells:
            if cell.cell_type != 'code':
                continue
            code_cells += 1
            if cell.execution_count is None:
                raise ValueError(f'{path.name}: unexecuted code cell {cell.id}')
            if any(out.output_type == 'error' for out in cell.outputs):
                raise ValueError(f'{path.name}: saved error in {cell.id}')
            figures += sum('image/png' in out.get('data', {}) for out in cell.outputs)
        if path.name.startswith('05'):
            live_cells = [c.source for c in nb.cells if c.cell_type == 'code' and 'RUN_LIVE =' in c.source]
            if not any('RUN_LIVE = False' in source for source in live_cells):
                raise ValueError('Reset lesson 05 to RUN_LIVE = False before sharing.')
    checked_links = 0
    broken = []
    pages = [p for p in files if p.suffix == '.html']
    for page in pages:
        soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        for tag in soup.select('[href], [src]'):
            value = tag.get('href', tag.get('src', ''))
            link = urlsplit(value)
            if link.scheme or link.netloc or not link.path:
                continue
            target = (page.parent/unquote(link.path)).resolve()
            checked_links += 1
            if target not in included:
                broken.append(f'{page.relative_to(root)} → {value}')
        if page.stem[:2].isdigit() and not soup.select_one('#show-code'):
            raise ValueError(f'{page.name}: reading controls missing; rebuild the HTML.')
    if broken:
        raise ValueError('Links missing from the public package:\n'+'\n'.join(broken))
    return files, {'notebooks': len(notebooks), 'executed_code_cells': code_cells,
                   'saved_figures': figures, 'html_pages': len(pages),
                   'checked_local_links': checked_links, 'live_api': 'disabled'}


def main():
    files, report = validate()
    output = ROOT/'dist'
    output.mkdir(exist_ok=True)
    archive = output/'jev-learning-public.zip'
    github_archive = output/'jev-learning-github.zip'
    for target, folder in [(archive,'jev-learning'),(github_archive,'jev-learning-course')]:
        with ZipFile(target, 'w', ZIP_DEFLATED) as bundle:
            for path in files:
                bundle.write(path, folder+'/'+path.relative_to(ROOT).as_posix())
    report.update(files=len(files), archive=archive.name, bytes=archive.stat().st_size,
                  github_archive=github_archive.name, github_bytes=github_archive.stat().st_size)
    (output/'package-validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
