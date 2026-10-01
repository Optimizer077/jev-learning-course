"""Exercise the Colab-only setup path locally, without opening a browser."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import ModuleType
from unittest.mock import patch

import nbformat
from course_paths import ROOT, NOTEBOOKS, NOTEBOOK_SETUP


def check_colab_setup():
    for path in NOTEBOOKS.glob('*.ipynb'):
        notebook = nbformat.read(path, as_version=4)
        first_code = next(c.source for c in notebook.cells if c.cell_type == 'code')
        assert first_code.startswith(NOTEBOOK_SETUP), path.name
        assert f'/notebooks/{path.name}' in notebook.cells[0].source, path.name

    with TemporaryDirectory(prefix='jev-colab-') as temporary:
        empty = Path(temporary) / 'runtime'
        empty.mkdir()
        clone = Path(temporary) / 'jev-learning-course'
        # Substitute only Colab's filesystem locations, preserving the setup logic.
        setup = NOTEBOOK_SETUP.replace('Path.cwd()', f'Path({str(empty)!r})')
        setup = setup.replace('Path("/content/jev-learning-course")', f'Path({str(clone)!r})')
        google = ModuleType('google')
        google.__path__ = []
        colab = ModuleType('google.colab')
        google.colab = colab

        def fetch_companions(arguments, **kwargs):
            assert arguments[:4] == ['git', 'clone', '--depth', '1']
            assert arguments[4] == 'https://github.com/Optimizer077/jev-learning-course.git'
            assert Path(arguments[5]) == clone
            assert kwargs == {'check': True}
            shutil.copytree(ROOT/'src', clone/'src')
            shutil.copytree(ROOT/'data', clone/'data')
            return subprocess.CompletedProcess(arguments, 0)

        original_path = sys.path.copy()
        try:
            namespace = {}
            with patch.dict(sys.modules, {'google':google, 'google.colab':colab}), \
                 patch('subprocess.run', side_effect=fetch_companions) as fetch:
                exec(setup, namespace)
            assert fetch.call_count == 1
            assert namespace['COURSE_ROOT'] == clone
            assert str(clone/'src') in sys.path
            spec = importlib.util.spec_from_file_location('colab_lab_core', clone/'src/lab_core.py')
            model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(model)
            assert len(model.load_tickets()) == 54
            assert list(model.softmax([0.0, 0.0])) == [0.5, 0.5]
            with patch.dict(sys.modules, {'google':google, 'google.colab':colab}), \
                 patch('subprocess.run') as fetch:
                exec(setup, {})
            assert fetch.call_count == 0, 'An existing complete clone should be reused'
            (clone/'data/tickets.json').unlink()
            with patch.dict(sys.modules, {'google':google, 'google.colab':colab}), \
                 patch('subprocess.run') as fetch:
                try:
                    exec(setup, {})
                except FileNotFoundError as error:
                    assert 'fresh runtime' in str(error)
                else:
                    raise AssertionError('An incomplete cached folder should get a clear setup error')
            assert fetch.call_count == 0, 'Do not clone into or overwrite an incomplete folder'
        finally:
            sys.path[:] = original_path
    print('Ten entry points; fresh Colab download, cached reuse, and incomplete-cache error passed. No browser opened.')


if __name__ == '__main__':
    check_colab_setup()
