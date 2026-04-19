import dash
import dash_bootstrap_components as dbc
from dash import clientside_callback, dcc, html, Input, Output

from ieee_papers_mapper.app.components.filters import build_filter_bar
from ieee_papers_mapper.app.queries import available_years


def _color_mode_switch() -> html.Span:
    return html.Span(
        [
            dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
            dbc.Switch(
                id="color-mode-switch",
                value=True,
                className="d-inline-block ms-1",
                persistence=True,
            ),
            dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
        ],
        className="d-flex align-items-center",
    )


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
                        dbc.NavItem(_color_mode_switch(), className="ms-3"),
                    ],
                    navbar=True,
                    className="align-items-center",
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
            dcc.Store(id="theme-store", data="light"),
            build_navbar(),
            dbc.Container(
                [
                    dcc.Store(id="filter-store", data={
                        "confidence": 0.5,
                        "categories": [],
                        "year_range": [min_year, max_year],
                    }),
                    build_filter_bar(),
                    dash.page_container,
                ],
                fluid=True,
                className="px-4",
            ),
        ]
    )


clientside_callback(
    """
    (switchOn) => {
        const theme = switchOn ? "light" : "dark";
        document.documentElement.setAttribute("data-bs-theme", theme);
        return theme;
    }
    """,
    Output("theme-store", "data"),
    Input("color-mode-switch", "value"),
)
