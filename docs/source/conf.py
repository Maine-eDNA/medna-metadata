# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'medna-metadata'
copyright = '2022, melkimble'
author = 'melkimble'

version = 'latest'
release = version


# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['.build']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'django': ('https://docs.djangoproject.com/en/4.0/', 'https://docs.djangoproject.com/en/4.0/_objects/'),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['.templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
