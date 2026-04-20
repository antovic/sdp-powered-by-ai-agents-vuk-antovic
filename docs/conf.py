"""Sphinx configuration file for Mars Rover Kata documentation."""

project = "Mars Rover Kata"
copyright = "2026, Vuk Antovic"
author = "Vuk Antovic"
release = "1.0.0"

extensions = [
    "sphinx_wagtail_theme",
    "myst_parser",
    "sphinx_new_tab_link",
]

new_tab_link_show_external_link_icon = True
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_wagtail_theme"
html_theme_options = {
    "project_name": "Mars Rover Kata",
    "github_url": "https://github.com/antovic/sdp-powered-by-ai-agents-vuk-antovic",
    "footer_links": "",
}

html_show_copyright = True
html_last_updated_fmt = "%b %d, %Y"
html_show_sphinx = False

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]
