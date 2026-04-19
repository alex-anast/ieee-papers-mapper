"""
Shared Filter Bar
=================

Renders confidence slider, category multi-select, and year range selector.
All pages read filter state from the dcc.Store populated by the shared callback.
"""

import dash_bootstrap_components as dbc
from dash import dcc, html

from ieee_papers_mapper.app.queries import available_categories, available_years


def build_filter_bar() -> dbc.Card:
    categories = available_categories()
    years = available_years()
    min_year = min(years) if years else 2024
    max_year = max(years) if years else 2025

    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Min Confidence", className="fw-bold small"),
                            dcc.Slider(
                                id="confidence-slider",
                                min=0,
                                max=1,
                                step=0.05,
                                value=0.5,
                                marks={
                                    v: f"{v:.1f}" for v in [0, 0.25, 0.5, 0.75, 1.0]
                                },
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            ),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [
                            html.Label("Categories", className="fw-bold small"),
                            dcc.Dropdown(
                                id="category-dropdown",
                                options=[
                                    {"label": c.title(), "value": c} for c in categories
                                ],
                                value=[],
                                multi=True,
                                placeholder="All categories",
                            ),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [
                            html.Label("Publication Year", className="fw-bold small"),
                            dcc.RangeSlider(
                                id="year-range",
                                min=min_year,
                                max=max_year,
                                step=1,
                                value=[min_year, max_year],
                                marks={
                                    y: str(y) for y in range(min_year, max_year + 1)
                                },
                                tooltip={
                                    "placement": "bottom",
                                    "always_visible": False,
                                },
                            ),
                        ],
                        md=4,
                    ),
                ],
                className="g-3 align-items-end",
            ),
        ),
        className="mb-4 shadow-sm",
    )
