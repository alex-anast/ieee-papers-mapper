import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from ieee_papers_mapper.app.components.filters import build_filter_bar
from ieee_papers_mapper.app.queries import available_years


def build_navbar() -> dbc.Navbar:
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(
                    "IEEE Papers Dashboard",
                    href="/",
                    className="fw-bold fs-4",
                ),
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Overview", href="/")),
                        dbc.NavItem(dbc.NavLink("Papers", href="/papers")),
                        dbc.NavItem(dbc.NavLink("Trends", href="/trends")),
                        dbc.NavItem(dbc.NavLink("Terms", href="/terms")),
                    ],
                    navbar=True,
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
        className="mb-3",
    )


def build_layout() -> html.Div:
    years = available_years()
    min_year = min(years) if years else 2024
    max_year = max(years) if years else 2025

    return html.Div(
        [
            build_navbar(),
            dbc.Container(
                [
                    dcc.Store(
                        id="filter-store",
                        data={
                            "confidence": 0.5,
                            "categories": [],
                            "year_range": [min_year, max_year],
                        },
                    ),
                    build_filter_bar(),
                    dash.page_container,
                ],
                fluid=True,
                className="px-4",
            ),
        ]
    )
