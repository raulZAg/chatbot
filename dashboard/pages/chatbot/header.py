from dash import html, dcc

def create_header():
    header = html.Div(
        children=[
            html.Div(
                children=[
                    html.H1(
                        children="Chatbot", className="header-title"
                    ),
                    html.P(
                        children=(
                            "DEMO Chatbot, active development"
                        ),
                        className="header-description",
                    ),
                    dcc.Link(
                        "Dashboard",
                        href="/",
                        className="link",
                    ),
                ],
                className="header",
            )
        ]
    )
    return header