import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, callback, dcc, html

from ieee_papers_mapper.app.app import CATEGORY_COLORS
from ieee_papers_mapper.app.components.kpi_card import kpi_card
from ieee_papers_mapper.app import queries

dash.register_page(__name__, path="/", name="Overview")


def _kpi_row() -> dbc.Row:
    kpis = queries.kpi_totals()
    return dbc.Row(
        [
            dbc.Col(kpi_card("Total Papers", kpis["total_papers"]), md=3),
            dbc.Col(kpi_card("Unique Authors", kpis["total_authors"]), md=3),
            dbc.Col(kpi_card("Avg Confidence", kpis["avg_confidence"]), md=3),
            dbc.Col(kpi_card("Affiliations", kpis["total_affiliations"]), md=3),
        ],
        className="mb-4 g-3",
    )


layout = html.Div(
    [
        html.H2("Overview", className="mb-3"),
        _kpi_row(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Loading(dcc.Graph(id="category-bar-chart"))),
                        className="shadow-sm",
                    ),
                    md=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Loading(dcc.Graph(id="confidence-box-plot"))),
                        className="shadow-sm",
                    ),
                    md=6,
                ),
            ],
            className="g-3",
        ),
    ]
)


@callback(
    Output("category-bar-chart", "figure"),
    Input("filter-store", "data"),
)
def update_category_bar(filters):
    df = queries.papers_by_category(
        confidence=filters.get("confidence", 0.5),
        categories=filters.get("categories") or None,
        year_range=filters.get("year_range") or None,
    )
    fig = px.bar(
        df,
        x="category",
        y="paper_count",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        text="paper_count",
        labels={"category": "Category", "paper_count": "Papers"},
        title="Papers by Category",
    )
    fig.update_layout(
        showlegend=False,
        transition_duration=300,
        margin=dict(t=40, b=30),
    )
    fig.update_traces(textposition="outside")
    return fig


@callback(
    Output("confidence-box-plot", "figure"),
    Input("filter-store", "data"),
)
def update_confidence_box(filters):
    df = queries.confidence_distribution(
        categories=filters.get("categories") or None,
        year_range=filters.get("year_range") or None,
    )
    fig = px.box(
        df,
        x="category",
        y="confidence",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        points="all",
        labels={"category": "Category", "confidence": "Confidence"},
        title="Classification Confidence Distribution",
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=40, b=30),
    )
    return fig
