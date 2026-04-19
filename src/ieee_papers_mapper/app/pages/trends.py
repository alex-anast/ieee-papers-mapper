import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, callback, dcc, html

from ieee_papers_mapper.app.app import CATEGORY_COLORS
from ieee_papers_mapper.app import queries

dash.register_page(__name__, path="/trends", name="Trends")

layout = html.Div(
    [
        html.H2("Trends", className="mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Loading(dcc.Graph(id="papers-over-time"))),
                        className="shadow-sm",
                    ),
                    md=12,
                    className="mb-3",
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Loading(dcc.Graph(id="downloads-vs-citations"))
                        ),
                        className="shadow-sm",
                    ),
                    md=12,
                ),
            ],
        ),
    ]
)


@callback(
    Output("papers-over-time", "figure"),
    Input("filter-store", "data"),
)
def update_time_series(filters):
    df = queries.papers_over_time(
        confidence=filters.get("confidence", 0.5),
        categories=filters.get("categories") or None,
        year_range=filters.get("year_range") or None,
    )
    if df.empty:
        fig = px.area(title="Papers Added Over Time")
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Papers",
            annotations=[
                dict(
                    text="No data for current filters",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="gray"),
                )
            ],
        )
        return fig

    fig = px.area(
        df,
        x="month",
        y="paper_count",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        labels={"month": "Month", "paper_count": "Papers", "category": "Category"},
        title="Papers Added Over Time",
    )
    fig.update_layout(
        margin=dict(t=40, b=30),
        hovermode="x unified",
    )
    return fig


@callback(
    Output("downloads-vs-citations", "figure"),
    Input("filter-store", "data"),
)
def update_scatter(filters):
    df = queries.downloads_vs_citations(
        confidence=filters.get("confidence", 0.5),
        categories=filters.get("categories") or None,
        year_range=filters.get("year_range") or None,
    )
    if df.empty:
        fig = px.scatter(title="Downloads vs Patent Citations")
        fig.update_layout(
            annotations=[
                dict(
                    text="No data for current filters",
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=16, color="gray"),
                )
            ],
        )
        return fig

    fig = px.scatter(
        df,
        x="download_count",
        y="citing_patent_count",
        color="category",
        color_discrete_map=CATEGORY_COLORS,
        size="confidence",
        hover_name="title",
        labels={
            "download_count": "Downloads",
            "citing_patent_count": "Patent Citations",
            "category": "Category",
            "confidence": "Confidence",
        },
        title="Downloads vs Patent Citations",
    )
    fig.update_layout(margin=dict(t=40, b=30))
    return fig
