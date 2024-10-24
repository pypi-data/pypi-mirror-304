extensions = [
    "jupyterlite_sphinx",
    "myst_parser",
]

myst_enable_extensions = [
    "linkify",
]

master_doc = "index"
source_suffix = ".rst"

project = "jupyterlite-xeus"
copyright = "JupyterLite Team"
author = "JupyterLite Team"

exclude_patterns = []

html_theme = "pydata_sphinx_theme"

html_static_path = ['_static']

html_css_files = [
    'css/custom.css',
]

jupyterlite_dir = "."

html_theme_options = {
    "logo": {
        "image_light": "jupyterlite.svg",
        "image_dark": "jupyterlite.svg",
    }
}
