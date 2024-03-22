from dash import dcc, html


def create_header():
    header = html.Div(
        children=[
            html.Div(
                children=[
                    html.H1(children="Dashboard Analytics", className="header-title"),
                    html.P(
                        children=("DEMO Dashboard, active development"),
                        className="header-description",
                    ),
                    # dcc.Link(
                    #    "Chatbot",
                    #    href="/chatbot",
                    #    className="link",
                    # ),
                ],
                className="header",
            )
        ]
    )
    return header
