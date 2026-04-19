"""
Reusable KPI Card
=================

A simple Bootstrap card that displays a metric label and value.
"""

import dash_bootstrap_components as dbc
from dash import html


def kpi_card(title: str, value) -> dbc.Card:
    return dbc.Card(
        dbc.CardBody(
            [
                html.P(title, className="text-muted mb-1 small"),
                html.H3(str(value), className="fw-bold mb-0"),
            ]
        ),
        className="shadow-sm text-center",
    )
