#!/usr/bin/env python3


"""
IEEE Papers Dashboard
=====================

A web-based dashboard using Dash to visualize paper counts by category from
the IEEE DuckDB database. Displays a bar chart that refreshes every 10 seconds
to reflect the latest classification data.

Functions
---------
- fetch_data(threshold: float = 0.5) -> pd.DataFrame
    Fetches paper counts grouped by category from the database.
- update_graph(n_intervals: int) -> go.Figure
    Callback that refreshes the bar chart with new data.
"""


import dash
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output
from ieee_papers_mapper.config import config as cfg
from ieee_papers_mapper.config.logging_config import setup_logging

setup_logging()


# Initialise the Dash app
app = dash.Dash(__name__)
app.title = "IEEE Papers Dashboard"


def fetch_data(threshold: float = 0.5) -> pd.DataFrame:
    """
    Fetches paper counts grouped by category from the database.

    Parameters
    ----------
    threshold : float, optional
        Minimum confidence score to filter the papers (default is 0.5).

    Returns
    -------
    pd.DataFrame
        DataFrame containing category and count of papers.
    """
    query = """
        SELECT c.category, COUNT(*) as paper_count
        FROM classification c
        JOIN papers p ON c.paper_id = p.paper_id
        WHERE c.confidence >= ?
        GROUP BY c.category
    """
    conn = duckdb.connect(cfg.DB_PATH, read_only=True)
    df = conn.execute(query, [threshold]).fetchdf()
    conn.close()
    return df


# Layout for the app
app.layout = html.Div(
    [
        html.H1("IEEE Papers by Category", style={"textAlign": "center"}),
        dcc.Graph(id="papers-bar-chart"),
        dcc.Interval(
            id="interval-component",
            interval=10 * 1000,  # Update every 10 seconds
            n_intervals=0,
        ),
    ]
)


# Callback to update graph
@app.callback(
    Output("papers-bar-chart", "figure"), [Input("interval-component", "n_intervals")]
)
def update_graph(n_intervals: int) -> go.Figure:
    """
    Updates the bar chart based on new data.

    Parameters
    ----------
    n_intervals : int
        Number of times the interval has fired.

    Returns
    -------
    go.Figure
        Updated bar chart.
    """
    df = fetch_data()
    fig = px.bar(
        df,
        x="category",
        y="paper_count",
        title="Papers by Category",
        labels={"category": "Category", "paper_count": "Number of Papers"},
        text="paper_count",
    )
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
