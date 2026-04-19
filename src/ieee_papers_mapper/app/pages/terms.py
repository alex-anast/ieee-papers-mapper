import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, callback, dcc, html

from ieee_papers_mapper.app import queries

dash.register_page(__name__, path="/terms", name="Term Analysis")

layout = html.Div(
    [
        html.H2("Term Analysis", className="mb-3"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Term Type", className="fw-bold small"),
                        dcc.Dropdown(
                            id="term-type-dropdown",
                            options=[
                                {"label": "All", "value": ""},
                                {"label": "IEEE Terms", "value": "IEEE"},
                                {"label": "Dynamic Terms", "value": "Dynamic"},
                            ],
                            value="",
                            clearable=False,
                        ),
                    ],
                    md=3,
                ),
                dbc.Col(
                    [
                        html.Label("Top N", className="fw-bold small"),
                        dcc.Slider(
                            id="top-n-slider",
                            min=5,
                            max=30,
                            step=5,
                            value=15,
                            marks={v: str(v) for v in [5, 10, 15, 20, 25, 30]},
                        ),
                    ],
                    md=3,
                ),
            ],
            className="mb-4 g-3 align-items-end",
        ),
        dbc.Card(
            dbc.CardBody(dcc.Loading(dcc.Graph(id="top-terms-chart"))),
            className="shadow-sm",
        ),
    ]
)


@callback(
    Output("top-terms-chart", "figure"),
    Input("filter-store", "data"),
    Input("term-type-dropdown", "value"),
    Input("top-n-slider", "value"),
)
def update_terms(filters, term_type, top_n):
    df = queries.top_terms(
        n=top_n or 15,
        term_type=term_type or None,
        confidence=filters.get("confidence", 0.5),
        categories=filters.get("categories") or None,
        year_range=filters.get("year_range") or None,
    )
    if df.empty:
        fig = px.bar(title="Top Index Terms")
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

    df = df.sort_values("freq", ascending=True)

    fig = px.bar(
        df,
        x="freq",
        y="term",
        color="term_type",
        orientation="h",
        text="freq",
        labels={"freq": "Frequency", "term": "Term", "term_type": "Type"},
        title=f"Top {len(df)} Index Terms",
        color_discrete_map={"IEEE": "#636EFA", "Dynamic": "#AB63FA"},
    )
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        margin=dict(t=40, l=200, b=30),
        legend_title_text="Term Type",
    )
    fig.update_traces(textposition="outside")
    return fig
