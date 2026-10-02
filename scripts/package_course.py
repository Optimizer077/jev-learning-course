"""Validate and zip the public course using an explicit file allowlist. Never uploads."""
import json
import ast
import base64
from pathlib import Path
from urllib.parse import unquote, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

import nbformat
from bs4 import BeautifulSoup

from course_paths import ROOT, NOTEBOOK_COUNT, html_references
ROOT_FILES = ['README.md', 'requirements.txt', '.gitignore', '.gitattributes', '.editorconfig']
PUBLIC_FOLDERS = {
    'notebooks': {'*.ipynb', '*.md'},
    'docs': {'*.md', 'validation.json', 'requirements-*.txt'},
    'assignments': {'*.md'},
    'data': {'*.md', 'tickets.json', 'torch_toy.json'},
    'src': {'*.py'},
    'scripts': {'*.py', '*.md'},
    'assets': {'*.svg', '*.png'},
    'site': {'*.html', '*.md'},
    '.github': {'*.yml', '*.md'},
}


def public_files(root=ROOT):
    files = [root/name for name in ROOT_FILES]
    for folder, patterns in PUBLIC_FOLDERS.items():
        for pattern in sorted(patterns):
            files += sorted((root/folder).rglob(pattern))
    missing = [str(p.relative_to(root)) for p in files if not p.is_file()]
    if missing:
        raise ValueError(f'Missing course files: {missing}. Build and execute the course first.')
    return sorted(set(files))


def validate(root=ROOT):
    files = public_files(root)
    included = {p.resolve() for p in files}
    notebooks = sorted((root/'notebooks').glob('[0-9][0-9]_*.ipynb'))
    if len(notebooks) != NOTEBOOK_COUNT:
        raise ValueError(f'Expected {NOTEBOOK_COUNT} lessons, found {len(notebooks)}.')
    code_cells = figures = diagrams = 0
    expected_artwork = []
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
            if 'show_diagram(' in cell.source:
                calls = [node for node in ast.walk(ast.parse(cell.source))
                         if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                         and node.func.id == 'show_diagram']
                for call in calls:
                    name, description = [ast.literal_eval(argument) for argument in call.args]
                    asset = root/'assets'/f'{name}.png'
                    if asset.resolve() not in included:
                        raise ValueError(f'{path.name}: companion artwork missing: {name}')
                    images = [out for out in cell.outputs if 'image/png' in out.get('data', {})]
                    if not any(base64.b64decode(out.data['image/png']) == asset.read_bytes()
                               and out.metadata.get('image/png', {}).get('alt') == description
                               for out in images):
                        raise ValueError(f'{path.name}: saved diagram or image description missing: {name}')
                    diagrams += 1
                    expected_artwork.append((path.stem, asset.read_bytes(), description))
        if path.name.startswith('05'):
            live_cells = [c.source for c in nb.cells if c.cell_type == 'code' and 'RUN_LIVE =' in c.source]
            if not any('RUN_LIVE = False' in source for source in live_cells):
                raise ValueError('Reset lesson 05 to RUN_LIVE = False before sharing.')
    checked_links = checked_sections = 0
    broken = []
    pages = [p for p in files if p.suffix == '.html']
    parsed = {page.resolve(): BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
              for page in pages}
    sections = {page: {tag['id'] for tag in soup.select('[id]')} |
                     {tag['name'] for tag in soup.select('a[name]')}
                for page, soup in parsed.items()}
    for stem, image, description in expected_artwork:
        page = (root/'site'/'lessons'/f'{stem}.html').resolve()
        source = 'data:image/png;base64,'+base64.b64encode(image).decode('ascii')
        if page not in parsed or not any(tag.get('src') == source and tag.get('alt') == description
                                         for tag in parsed[page].select('img')):
            raise ValueError(f'{stem}: embedded HTML artwork or authored description missing')
    for page in pages:
        soup = parsed[page.resolve()]
        for value in (url for tag in soup.select('[href], [src], [srcset]') for url in html_references(tag)):
            link = urlsplit(value)
            if link.scheme or link.netloc:
                continue
            target = (page.parent/unquote(link.path)).resolve() if link.path else page.resolve()
            checked_links += bool(link.path)
            if target not in included:
                broken.append(f'{page.relative_to(root)} → {value}')
            elif link.fragment and target in sections:
                checked_sections += 1
                if unquote(link.fragment) not in sections[target]:
                    broken.append(f'{page.relative_to(root)} → missing section {value}')
        if page.stem[:2].isdigit() and not soup.select_one('#show-code'):
            raise ValueError(f'{page.name}: reading controls missing; rebuild the HTML.')
    if broken:
        raise ValueError('Links missing from the public package:\n'+'\n'.join(broken))
    return files, {'notebooks': len(notebooks), 'executed_code_cells': code_cells,
                   'saved_figures': figures, 'html_pages': len(pages),
                   'embedded_teaching_diagrams': diagrams,
                   'checked_local_links': checked_links, 'checked_section_links': checked_sections,
                   'live_api': 'disabled'}


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
