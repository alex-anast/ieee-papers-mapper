import dash
import dash_bootstrap_components as dbc

CATEGORY_COLORS = {
    "machine learning": "#636EFA",
    "power electronics": "#EF553B",
    "robotics": "#00CC96",
}

app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder="pages",
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    title="IEEE Papers Dashboard",
)
server = app.server
