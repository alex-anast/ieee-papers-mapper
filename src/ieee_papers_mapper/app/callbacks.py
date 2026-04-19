"""
Shared Callbacks
================

Registers application-wide callbacks that are not page-specific,
such as filter-state synchronization across pages.
"""

from dash import Dash, Input, Output


def register_callbacks(app: Dash) -> None:
    @app.callback(
        Output("filter-store", "data"),
        [
            Input("confidence-slider", "value"),
            Input("category-dropdown", "value"),
            Input("year-range", "value"),
        ],
    )
    def sync_filters(confidence, categories, year_range):
        if categories is None:
            categories = []
        if year_range is None:
            year_range = []
        return {
            "confidence": confidence,
            "categories": categories,
            "year_range": year_range,
        }
