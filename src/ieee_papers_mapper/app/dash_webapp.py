#!/usr/bin/env python3


"""
IEEE Papers Dashboard
=====================

This script creates a web-based dashboard using Dash to visualize paper counts by category from an IEEE database.
The dashboard fetches data from a SQLite database and displays a bar chart showing the number of papers in each category.
The chart is updated every 10 seconds to reflect the latest data.

Key Components:
---------------
1. **Dash Web App**: A basic web interface created with Dash that includes a bar chart visualizing paper counts.
2. **Database Interaction**: Fetches paper count data grouped by category from a SQLite database, with a confidence threshold filter.
3. **Real-time Updates**: The bar chart updates every 10 seconds to display real-time changes in paper counts.

Functions:
----------
- `fetch_data(threshold: float = 0.5) -> pd.DataFrame`: Fetches paper counts grouped by category from the database.
- `update_graph(n_intervals: int) -> plotly.graph_objects.Figure`: Callback function to update the bar chart with new data.

Usage:
------
- Run the script to start the web application.
- The app fetches and displays data from the database, and automatically updates the bar chart every 10 seconds.

Example:
--------
- The web page will display the number of papers in each category where the confidence score is above a given threshold (default 0.5).
"""


import dash
import pandas as pd
import sqlite3
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from src.ieee_papers_mapper.config import config as cfg


# Initialise the Dash app
app = dash.Dash(__name__)
app.title = "IEEE Papers Dashboard"


def fetch_data(threshold: float = 0.5) -> pd.DataFrame:
    """
    Fetches paper counts grouped by category from the database.

    Parameters:
    ----------
    threshold : float, optional
        Minimum confidence score to filter the papers (default is 0.5).

    Returns:
    -------
    pd.DataFrame
        DataFrame containing category and count of papers.
    """
    query = f"""
        SELECT c.category, COUNT(*) as paper_count
        FROM classification c
        JOIN papers p ON c.paper_id = p.paper_id
        WHERE c.confidence >= {threshold}  -- Filter rows before grouping
        GROUP BY c.category
    """
    conn = sqlite3.connect(cfg.DB_PATH)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# Layout for the app
app.layout = html.Div([
    html.H1("IEEE Papers by Category", style={"textAlign": "center"}),
    dcc.Graph(id="papers-bar-chart"),
    dcc.Interval(
        id="interval-component",
        interval=10 * 1000,  # Update every 10 seconds
        n_intervals=0
    )
])


# Callback to update graph
@app.callback(
    Output("papers-bar-chart", "figure"),
    [Input("interval-component", "n_intervals")]
)
def update_graph(n_intervals):  # TODO: missing type hint and return type
    """
    Updates the bar chart based on new data.

    Parameters:
    ----------
    n_intervals : int
        Number of times the interval has fired.

    Returns:
    -------
    plotly.graph_objects.Figure:
        Updated bar chart.
    """
    df = fetch_data()
    fig = px.bar(
        df,
        x="category",
        y="paper_count",
        title="Papers by Category",
        labels={"category": "Category", "paper_count": "Number of Papers"},
        text="paper_count"
    )
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)

