"""Offline checks for the GitHub course, notebook links, and packaged saved output."""
import ast
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

import mistune
import nbformat
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from package_course import ROOT, validate


def markdown_urls(nodes):
    for node in nodes:
        if node.get('type') in {'link', 'image'}:
            yield node['attrs']['url']
        if node.get('type') in {'inline_html', 'block_html'}:
            fragment = BeautifulSoup(node.get('raw', ''), 'html.parser')
            for tag in fragment.select('[href], [src]'):
                yield tag.get('href', tag.get('src', ''))
        yield from markdown_urls(node.get('children', []))


def validate_github_course(root=ROOT):
    files, report = validate(root)
    included = {path.resolve() for path in files}
    parse = mistune.create_markdown(renderer='ast', plugins=['table'])
    broken = []
    count = 0
    colab_links = 0
    python_files = 0
    documents = []
    for path in files:
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            python_files += 1
        if path.suffix == '.svg':
            ET.parse(path)
        if path.suffix == '.md':
            documents.append((path, path.read_text(encoding='utf-8')))
        if path.suffix == '.ipynb':
            notebook = nbformat.read(path, as_version=4)
            for cell in notebook.cells:
                if cell.cell_type == 'markdown':
                    documents.append((path, cell.source))
    for path, source in documents:
        for url in markdown_urls(parse(source)):
            link = urlsplit(url)
            if link.netloc == 'colab.research.google.com' and link.path.startswith('/github/'):
                colab_links += 1
                prefix = '/github/Optimizer077/jev-learning-course/blob/main/'
                if not link.path.startswith(prefix):
                    broken.append(f'{path.relative_to(root)}: unexpected Colab repository')
                else:
                    target = (root / unquote(link.path[len(prefix):])).resolve()
                    if target not in included or target.suffix != '.ipynb':
                        broken.append(f'{path.relative_to(root)}: missing Colab lesson')
            if link.scheme or link.netloc or not link.path:
                continue
            count += 1
            target = (path.parent / unquote(link.path)).resolve()
            if target not in included:
                broken.append(f'{path.relative_to(root)} → {url}')
    if broken:
        raise ValueError('Local Markdown links missing from the course:\n'+'\n'.join(broken))
    report.update(checked_markdown_links=count, checked_colab_links=colab_links,
                  checked_python_sources=python_files,
                  github_configuration='included', validation_mode='offline; no external URLs requested')
    return report


if __name__ == '__main__':
    print(json.dumps(validate_github_course(), indent=2))
