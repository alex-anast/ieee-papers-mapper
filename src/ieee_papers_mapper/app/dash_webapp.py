#!/usr/bin/env python3

"""
IEEE Papers Dashboard
=====================

Entry point for the Dash application. Imports the shared Dash instance,
applies the top-level layout (navbar + page container), and registers
all page-level callbacks via module imports.
"""

from ieee_papers_mapper.app.app import app
from ieee_papers_mapper.app.layout import build_layout
from ieee_papers_mapper.app.callbacks import register_callbacks
from ieee_papers_mapper.config.logging_config import setup_logging

setup_logging()

app.layout = build_layout()
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
