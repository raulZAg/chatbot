import dash
from dash import html, Input, Output
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__,use_pages=True, update_title="Loading ...", external_stylesheets=external_stylesheets)
server = app.server

# Crear el layout
app.layout = html.Div(
    children=[
        dash.page_container,
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)

