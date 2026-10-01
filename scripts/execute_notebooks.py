"""Execute each notebook in a fresh kernel and export its saved output."""
import json
from pathlib import Path
import importlib.metadata
from time import perf_counter
import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from build_site import build_site, style_lesson

from course_paths import ROOT, NOTEBOOKS, DOCS, EXPORTS
root = ROOT
EXPORTS.mkdir(parents=True, exist_ok=True)
results = []
paths = sorted(NOTEBOOKS.glob('[0-9][0-9]_*.ipynb'))
for path in paths:
    started = perf_counter()
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    NotebookClient(notebook, timeout=180, kernel_name='python3',
                   resources={'metadata': {'path': str(NOTEBOOKS)}}).execute()
    nbformat.write(notebook, path)
    html, _ = HTMLExporter().from_notebook_node(notebook)
    html = style_lesson(html, path.stem, [p.stem for p in paths],
                        source_path=path.relative_to(ROOT).as_posix(), notebook=notebook)
    (EXPORTS / f'{path.stem}.html').write_text(html, encoding='utf-8')
    result = {'notebook': path.name, 'code_cells': sum(c.cell_type == 'code' for c in notebook.cells),
              'executed': True, 'seconds': round(perf_counter()-started,2),
              'figures': sum('image/png' in o.get('data',{}) for c in notebook.cells for o in c.get('outputs',[])),
              'live_api': ('skipped' if any('LIVE REQUEST SKIPPED' in out.get('text', '')
                                           for c in notebook.cells for out in c.get('outputs', []))
                           else 'enabled; inspect saved response') if path.name.startswith('05') else 'not used'}
    results.append(result)
    print(result, flush=True)
(DOCS / 'validation.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
packages = ['numpy', 'matplotlib', 'nbformat', 'nbclient', 'nbconvert', 'ipykernel', 'jupyterlab', 'beautifulsoup4', 'mistune']
(DOCS / 'requirements-tested.txt').write_text('\n'.join(f'{p}=={importlib.metadata.version(p)}' for p in packages) + '\n', encoding='utf-8')
build_site()
