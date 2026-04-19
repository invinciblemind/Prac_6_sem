import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath('../mood'))
sys.path.insert(0, os.path.abspath('../mood/server'))

project = 'MUD (client-server)'
copyright = f'2026, Max G'
author = 'Max G'
release = '1.0.0'
version = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
]

autodoc_mock_imports = ['cowsay', 'asyncio', 'threading', 'shlex']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']

# Настройки autodoc
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}
