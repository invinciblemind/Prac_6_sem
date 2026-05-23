#!/usr/bin/env python3
# dodo.py - DoIt automation for MUD project

import glob
from pathlib import Path
import shutil
import os

DOIT_CONFIG = {
    'default_tasks': ['html'],
}


def clean_targets(targets):
    """Remove generated files and directories."""
    for t in targets:
        path = Path(t)
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        elif path.exists():
            path.unlink()


def task_extract():
    """Extract translatable strings into .pot file."""
    pot_file = 'mood/server/tra.pot'
    source_dirs = ['mood/server', 'mood/client']
    # Collect all Python source files as dependencies
    file_dep = []
    for d in source_dirs:
        file_dep.extend(glob.glob(f'{d}/**/*.py', recursive=True))

    return {
        'actions': [
            f'pybabel extract -F babel.cfg -o {pot_file} {" ".join(source_dirs)}'
        ],
        'file_dep': file_dep,
        'targets': [pot_file],
        'clean': [clean_targets],
    }


def task_update():
    """Обновление .po файла из .pot."""
    pot_file = 'mood/server/tra.pot'
    po_dir = 'mood/server/po'
    po_file = 'mood/server/po/ru_RU/LC_MESSAGES/tra.po'

    return {
        'actions': [
            f'pybabel update -i {pot_file} -d {po_dir} -l ru_RU -D tra'
        ],
        'file_dep': [pot_file],   # зависим только от .pot
        'targets': [po_file],
        'clean': [],              # .po - исходный файл, не удаляем
    }


def task_compile():
    """Compile .po file into .mo binary catalog."""
    po_dir = 'mood/server/po'
    mo_file = 'mood/server/po/ru_RU/LC_MESSAGES/tra.mo'

    return {
        'actions': [
            f'pybabel compile -d {po_dir} -l ru_RU -D tra -f'
        ],
        'file_dep': ['mood/server/po/ru_RU/LC_MESSAGES/tra.po'],
        'targets': [mo_file],
        'clean': [clean_targets],
    }


def task_i18n():
    """Full internationalization pipeline: extract → update → compile."""
    return {
        'task_dep': ['extract', 'update', 'compile'],
        'actions': [],
        'clean': [],
    }


def task_html():
    """Generate HTML documentation with Sphinx."""
    build_dir = 'doc/_build'
    index_html = f'{build_dir}/html/index.html'
    file_dep = (
        glob.glob('doc/*.rst') +
        glob.glob('doc/conf.py') +
        glob.glob('mood/**/*.py', recursive=True)
    )

    return {
        'actions': [
            f'sphinx-build -b html doc {build_dir}/html'
        ],
        'file_dep': file_dep,
        'targets': [index_html],
        'clean': [clean_targets],
    }


def task_copy_docs():
    """Копировать сгенерированную HTML-документацию в пакет mood/html."""
    src = 'doc/_build/html'
    dst = 'mood/html'
    return {
        'actions': [
            (shutil.rmtree, [dst], {'ignore_errors': True}),
            (shutil.copytree, [src, dst]),
        ],
        'file_dep': ['doc/_build/html/index.html'],
        'targets': [f'{dst}/index.html'],
        'clean': [(clean_targets, [[dst]])],
    }


def task_wheel():
    """Собрать бинарный дистрибутив (wheel)."""
    return {
        'actions': ['python -m build --wheel'],
        'task_dep': ['i18n', 'copy_docs'],   # copy_docs зависит от html
        'file_dep': ['pyproject.toml', 'MANIFEST.in'],
        'targets': ['dist/*.whl'],
        'clean': [(clean_targets, [['dist']])],
    }


def task_sdist():
    """Собрать исходный дистрибутив (sdist)."""
    return {
        'actions': ['python -m build --sdist'],
        'task_dep': ['clean_all'],   # очистить все генераты перед сборкой
        'file_dep': ['pyproject.toml', 'MANIFEST.in'],
        'targets': ['dist/*.tar.gz'],
        'clean': [(clean_targets, [['dist']])],
    }


def task_clean_all():
    """Удалить все сгенерированные файлы (pot, mo, docs, dist, mood/html)."""
    return {
        'actions': [
            (clean_targets, [[
                'mood/server/tra.pot',
                'mood/server/po/ru_RU/LC_MESSAGES/tra.mo',
                'doc/_build',
                'mood/html',
                'dist'
            ]]),
        ],
    }


def task_test():
    """Run unit tests (depends on i18n because tests may check localized replies)."""
    return {
        'actions': ['python -m unittest testing.py'],
        'task_dep': ['i18n'],
        'file_dep': [
            'testing.py',
            'mood/server/server.py',
            'mood/client/__main__.py',
        ],
        'clean': [],
    }
