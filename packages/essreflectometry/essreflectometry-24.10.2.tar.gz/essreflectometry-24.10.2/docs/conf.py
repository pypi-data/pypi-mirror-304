# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2024 Scipp contributors (https://github.com/scipp)

import doctest
import os
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as get_version

from sphinx.util import logging

sys.path.insert(0, os.path.abspath('.'))

logger = logging.getLogger(__name__)

# General information about the project.
project = 'ESSreflectometry'
copyright = '2024 Scipp contributors'
author = 'Scipp contributors'

html_show_sourcelink = True

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
    'sphinx_copybutton',
    'sphinx_design',
    'nbsphinx',
    'myst_parser',
]

try:
    import sciline.sphinxext.domain_types  # noqa: F401

    extensions.append('sciline.sphinxext.domain_types')
    # See https://github.com/tox-dev/sphinx-autodoc-typehints/issues/457
    suppress_warnings = ["config.cache"]
except ModuleNotFoundError:
    pass


myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_heading_anchors = 3

autodoc_type_aliases = {
    'array_like': 'array_like',
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipp': ('https://scipp.github.io/', None),
}

# autodocs includes everything, even irrelevant API internals. autosummary
# looks more suitable in the long run when the API grows.
# For a nice example see how xarray handles its API documentation.
autosummary_generate = True

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_param = True
napoleon_use_rtype = False
napoleon_preprocess_types = True
napoleon_type_aliases = {
    # objects without namespace: numpy
    "ndarray": "~numpy.ndarray",
}
typehints_defaults = 'comma'
typehints_use_rtype = False

sciline_domain_types_prefix = 'ess.reflectometry'
sciline_domain_types_aliases = {
    'scipp._scipp.core.DataArray': 'scipp.DataArray',
    'scipp._scipp.core.Dataset': 'scipp.Dataset',
    'scipp._scipp.core.DType': 'scipp.DType',
    'scipp._scipp.core.Unit': 'scipp.Unit',
    'scipp._scipp.core.Variable': 'scipp.Variable',
    'scipp.core.data_group.DataGroup': 'scipp.DataGroup',
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']
html_sourcelink_suffix = ''  # Avoid .ipynb.txt extensions in sources

# The master toctree document.
master_doc = 'index'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#

try:
    release = get_version("essreflectometry")
    version = ".".join(release.split('.')[:3])  # CalVer
except PackageNotFoundError:
    logger.info(
        "Warning: determining version from package metadata failed, falling back to "
        "a dummy version number."
    )
    release = version = "0.0.0-dev"

warning_is_error = True

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "primary_sidebar_end": ["edit-this-page", "sourcelink"],
    "secondary_sidebar_items": [],
    "navbar_persistent": ["search-button"],
    "show_nav_level": 1,
    # Adjust this to ensure external links are moved to "Move" menu
    "header_links_before_dropdown": 4,
    "pygment_light_style": "github-light-high-contrast",
    "pygment_dark_style": "github-dark-high-contrast",
    "logo": {
        "image_light": "_static/logo.svg",
        "image_dark": "_static/logo-dark.svg",
    },
    "external_links": [
        {"name": "Plopp", "url": "https://scipp.github.io/plopp"},
        {"name": "Sciline", "url": "https://scipp.github.io/sciline"},
        {"name": "Scipp", "url": "https://scipp.github.io"},
        {"name": "ScippNeutron", "url": "https://scipp.github.io/scippneutron"},
        {"name": "ScippNexus", "url": "https://scipp.github.io/scippnexus"},
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/scipp/essreflectometry",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/essreflectometry/",
            "icon": "fa-brands fa-python",
            "type": "fontawesome",
        },
        {
            "name": "Conda",
            "url": "https://anaconda.org/scipp/essreflectometry",
            "icon": "fa-custom fa-anaconda",
            "type": "fontawesome",
        },
    ],
    "footer_start": ["copyright", "sphinx-version"],
    "footer_end": ["doc_version", "theme-version"],
}
html_context = {
    "doc_path": "docs",
}
html_sidebars = {
    "**": ["sidebar-nav-bs", "page-toc"],
}

html_title = "ESSreflectometry"
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.svg"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = []
html_js_files = ["anaconda-icon.js"]

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'essreflectometrydoc'

# -- Options for Matplotlib in notebooks ----------------------------------

nbsphinx_execute_arguments = [
    "--Session.metadata=scipp_sphinx_build=True",
]

# -- Options for doctest --------------------------------------------------

# sc.plot returns a Figure object and doctest compares that against the
# output written in the docstring. But we only want to show an image of the
# figure, not its `repr`.
# In addition, there is no need to make plots in doctest as the documentation
# build already tests if those plots can be made.
# So we simply disable plots in doctests.
doctest_global_setup = '''
import numpy as np

try:
    import scipp as sc

    def do_not_plot(*args, **kwargs):
        pass

    sc.plot = do_not_plot
    sc.Variable.plot = do_not_plot
    sc.DataArray.plot = do_not_plot
    sc.DataGroup.plot = do_not_plot
    sc.Dataset.plot = do_not_plot
except ImportError:
    # Scipp is not needed by docs if it is not installed.
    pass
'''

# Using normalize whitespace because many __str__ functions in scipp produce
# extraneous empty lines and it would look strange to include them in the docs.
doctest_default_flags = (
    doctest.ELLIPSIS
    | doctest.IGNORE_EXCEPTION_DETAIL
    | doctest.DONT_ACCEPT_TRUE_FOR_1
    | doctest.NORMALIZE_WHITESPACE
)

# -- Options for linkcheck ------------------------------------------------

linkcheck_ignore = [
    # Specific lines in Github blobs cannot be found by linkcheck.
    r'https?://github\.com/.*?/blob/[a-f0-9]+/.+?#',
]
