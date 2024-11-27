import dash
from dash import dcc, html
import pandas as pd
import sqlite3
import plotly.express as px

# Connect to the database
DB_PATH = "./data/ieee_papers.db"
conn = sqlite3.connect(DB_PATH)

# Query the classification data
query = """
SELECT c.paper_id, p.title, c.category, c.confidence
FROM classification c
JOIN papers p ON c.paper_id = p.paper_id
"""
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Initialize Dash app
app = dash.Dash(__name__)

# Layout for the dashboard
app.layout = html.Div(
    children=[
        html.H1(children="IEEE Papers Classification Dashboard"),
        html.Div(children="A dashboard to visualize classified papers."),
        dcc.Graph(
            id="classification-bar-chart",
            figure=px.bar(
                df,
                x="category",
                y="confidence",
                color="category",
                title="Confidence Scores by Category",
                labels={"confidence": "Confidence Score", "category": "Category"},
            ),
        ),
        dcc.Graph(
            id="paper-count-pie-chart",
            figure=px.pie(
                df, names="category", title="Distribution of Papers by Category"
            ),
        ),
        dcc.Graph(
            id="confidence-histogram",
            figure=px.histogram(
                df,
                x="confidence",
                color="category",
                title="Confidence Score Distribution",
                nbins=20,
            ),
        ),
    ]
)

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
