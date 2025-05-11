# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('./homogen'))

project = 'Machine Perception and Tracking - Praktikum'
copyright = '2025, Prof. Dr. Dennis Müller'
author = 'Prof. Dr. Dennis Müller'

extensions = ['myst_parser', 
              'sphinx.ext.autodoc', 
              'sphinx.ext.autosummary', 
              'sphinx.ext.intersphinx',
              'sphinx.ext.viewcode',
              'sphinxcontrib.mermaid',
              'sphinx.ext.mathjax',
              'sphinx_togglebutton']

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

language = 'de'

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'canonical_url': '',
}
html_baseurl = 'https://dmu1981.github.io/MPTPraktikum/'