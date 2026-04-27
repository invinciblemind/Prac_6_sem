#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile
DOIT_CONFIG = {"default_tasks": ['docs']}


def task_docs():
    """Create documentation"""
    rstpy = list(Path('.').glob('**/*.rst')) + list(Path('.').glob('**/*.py'))
    return {
        'actions': ["make -C doc html"],
        'targets': ['doc/_build/html/index.html'],
        'file_dep': rstpy,
    }


def task_erase():
    """Clean all junk"""
    
    return {
        "actions": ["rm -rf doc/_build *.zip"],
    }


def task_zip():
    """Make zip of docs"""
    
    def create_zip(filename, files):
        print('!!!', filename, files)
        with ZipFile(filename, 'w') as zf:
            for f in files:
                zf.write(f)
    
    files = list(Path('doc/_build/html').glob('**'))
    
    print('@@@')
    
    # create_zip('docs.zip', files)
    
    return {
        "actions": [(create_zip, ['docs.zip', files])],
        'task_dep': ['docs'],
    }
