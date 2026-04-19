import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dash_table, dcc, html

from ieee_papers_mapper.app import queries

dash.register_page(__name__, path="/papers", name="Papers")

TABLE_COLUMNS = [
    {"name": "Title", "id": "title", "type": "text"},
    {"name": "Category", "id": "category", "type": "text"},
    {"name": "Confidence", "id": "confidence", "type": "numeric"},
    {"name": "Year", "id": "publication_year", "type": "numeric"},
    {"name": "Downloads", "id": "download_count", "type": "numeric"},
    {"name": "Patent Cites", "id": "citing_patent_count", "type": "numeric"},
    {"name": "Authors", "id": "authors", "type": "text"},
]

_LIGHT_TABLE_STYLE = {
    "header_bg": "#f8f9fa",
    "cell_bg": "white",
    "cell_color": "#212529",
    "selected_bg": "#e2e6ea",
    "selected_border": "1px solid #2c7be5",
    "filter_bg": "white",
    "filter_color": "#212529",
}

_DARK_TABLE_STYLE = {
    "header_bg": "#2b3035",
    "cell_bg": "#212529",
    "cell_color": "#dee2e6",
    "selected_bg": "#3a4149",
    "selected_border": "1px solid #6ea8fe",
    "filter_bg": "#2b3035",
    "filter_color": "#dee2e6",
}

layout = html.Div(
    [
        html.H2("Papers Explorer", className="mb-3"),
        dbc.Card(
            dbc.CardBody(
                dcc.Loading(
                    dash_table.DataTable(
                        id="papers-table",
                        columns=TABLE_COLUMNS,
                        page_size=15,
                        sort_action="native",
                        filter_action="native",
                        row_selectable="single",
                        style_table={"overflowX": "auto"},
                        style_cell={
                            "textAlign": "left",
                            "padding": "8px 12px",
                            "fontFamily": "inherit",
                            "whiteSpace": "normal",
                            "height": "auto",
                        },
                        style_cell_conditional=[
                            {"if": {"column_id": "title"}, "minWidth": "280px"},
                            {"if": {"column_id": "authors"}, "minWidth": "200px"},
                        ],
                    )
                )
            ),
            className="shadow-sm mb-3",
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="detail-title")),
                dbc.ModalBody(id="detail-body"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-detail", className="ms-auto")
                ),
            ],
            id="detail-modal",
            size="lg",
            is_open=False,
        ),
    ]
)


@callback(
    Output("papers-table", "data"),
    Output("papers-table", "style_header"),
    Output("papers-table", "style_data"),
    Output("papers-table", "style_data_conditional"),
    Output("papers-table", "style_filter"),
    Input("filter-store", "data"),
    Input("theme-store", "data"),
)
def update_table(filters, theme):
    df = queries.papers_table(
        confidence=filters.get("confidence", 0.5),
        categories=filters.get("categories") or None,
        year_range=filters.get("year_range") or None,
    )

    s = _DARK_TABLE_STYLE if theme == "dark" else _LIGHT_TABLE_STYLE

    style_header = {
        "fontWeight": "bold",
        "backgroundColor": s["header_bg"],
        "color": s["cell_color"],
    }
    style_data = {
        "backgroundColor": s["cell_bg"],
        "color": s["cell_color"],
    }
    style_cond = [
        {
            "if": {"state": "selected"},
            "backgroundColor": s["selected_bg"],
            "border": s["selected_border"],
        },
    ]
    style_filter = {
        "backgroundColor": s["filter_bg"],
        "color": s["filter_color"],
    }

    return df.to_dict("records"), style_header, style_data, style_cond, style_filter


@callback(
    Output("detail-modal", "is_open"),
    Output("detail-title", "children"),
    Output("detail-body", "children"),
    Input("papers-table", "selected_rows"),
    State("papers-table", "data"),
    Input("close-detail", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_detail(selected_rows, table_data, close_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, "", ""

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "close-detail":
        return False, "", ""

    if not selected_rows:
        return False, "", ""

    row = table_data[selected_rows[0]]
    paper_id = row.get("paper_id")
    if paper_id is None:
        return False, "", ""

    detail = queries.paper_detail(paper_id)
    if not detail:
        return False, "", ""

    author_items = [
        html.Li(f"{a['name']} — {a['affiliation']}") for a in detail["authors"]
    ]

    ieee_terms = [t["term"] for t in detail["terms"] if t["term_type"] == "IEEE"]
    dynamic_terms = [t["term"] for t in detail["terms"] if t["term_type"] == "Dynamic"]

    body = html.Div(
        [
            dbc.Badge(detail["category"].title(), color="primary", className="mb-2 me-2"),
            dbc.Badge(f"Confidence: {detail['confidence']}", color="info", className="mb-2"),
            html.H6("Abstract", className="mt-3"),
            html.P(detail["abstract"], className="text-muted"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Small("Year", className="text-muted"),
                            html.P(detail["publication_year"], className="fw-bold"),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [
                            html.Small("Downloads", className="text-muted"),
                            html.P(f"{detail['download_count']:,}", className="fw-bold"),
                        ],
                        md=4,
                    ),
                    dbc.Col(
                        [
                            html.Small("Patent Citations", className="text-muted"),
                            html.P(detail["citing_patent_count"], className="fw-bold"),
                        ],
                        md=4,
                    ),
                ],
                className="mb-3",
            ),
            html.H6("Authors"),
            html.Ul(author_items) if author_items else html.P("—"),
            html.H6("IEEE Terms"),
            html.P(", ".join(ieee_terms) if ieee_terms else "—"),
            html.H6("Dynamic Terms"),
            html.P(", ".join(dynamic_terms) if dynamic_terms else "—"),
        ]
    )

    return True, detail["title"], body
