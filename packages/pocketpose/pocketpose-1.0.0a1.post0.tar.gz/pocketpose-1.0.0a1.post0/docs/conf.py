# Configuration file for the Sphinx documentation builder.

# -- Path setup
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project information
project = "PocketPose"
copyright = "2024, Muhammad Saif Ullah Khan"
author = "Muhammad Saif Ullah Khan"

# Import the version from the __version__ variable in the package

# The full version, including alpha/beta/rc tags
version_file = "../VERSION"


def get_version():
    with open(version_file, "r") as f:
        return f.read().strip()


release = get_version()

# -- General configuration
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.mermaid",
    "sphinx_copybutton",
    "myst_parser",
    "autoapi.extension",
]

# Document Python Code
autoapi_type = "python"
autoapi_root = "generated"
autoapi_dirs = ["../pocketpose"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

html_static_path = ["_static"]
templates_path = ["_templates"]

# -- Options for HTML output
html_theme = "furo"
html_theme_options = {
    "light_logo": "images/logo.svg",
    "dark_logo": "images/logo-dark.svg",
    "source_repository": "https://github.com/saifkhichi96/pocket-pose/",
    "source_branch": "main",
    "source_directory": "docs/",
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#1898F3",
        "color-brand-content": "#1898F3",
        "color-background-secondary": "#f6fdff",
        "color-background-border": "#deecf0",
        "font-stack": "Hind Siliguri, Roboto Condensed, Arial, sans-serif",
    },
    "dark_css_variables": {
        "color-brand-primary": "#1898F3",
        "color-brand-content": "#1898F3",
        "font-stack": "Hind Siliguri, Roboto Condensed, Arial, sans-serif",
    },
}
html_css_files = [
    "https://fonts.googleapis.com/css2?family=Hind+Siliguri&family=Roboto+Condensed:wght@300;400;700&display=swap"
]
html_sidebars = {
    "**": [
        "sidebar/brand.html",
        "sidebar/search.html",
        "sidebar/scroll-start.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html",
        "sidebar/variant-selector.html",
    ]
}

# -- Options for EPUB output
epub_show_urls = "footnote"
