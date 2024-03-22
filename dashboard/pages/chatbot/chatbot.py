import dash
from textwrap import dedent
from dash import dcc, html, Input, Output, callback, State, get_asset_url
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pages.chatbot.header as header
import openai
from dotenv import load_dotenv
import os

# Registrar la página en Dash
dash.register_page(
    __name__,
    path="/chatbot",
    title="Chatbot",
    name="Chatbot",
    description="A Demo Chatbot for Sale",
)

description = """
"José is an assistant for technology companies. He is extremely polite, professional, and serious. He always provides direct answers and never makes up stories. If he doesn't know something, he acknowledges it."
"""

# Authentication
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Función para crear el menú del chatbot
def create_chat_menu():
    menu = html.Div(
        children=[
            html.Div(children="Select API", className="menu-title"),
            dcc.Dropdown(
                id="api-filter",
                options=[
                    {"label": "OpenAI API", "value": "openai"},
                    {"label": "Azure API", "value": "azure"},
                ],
                value="openai",
                clearable=False,
                className="dropdown",
            ),
            html.Div(children="Select User Type", className="menu-title"),
            dcc.Dropdown(
                id="user-type-filter",
                options=[
                    {"label": "Salesteam", "value": "salesteam"},
                    {"label": "Human Resources", "value": "hhrr"},
                ],
                value="hhrr",
                clearable=False,
                className="dropdown",
            ),
        ],
        className="chatbot-menu",
    )
    return menu

def textbox(text, box="AI", name="Jose Carlos"):
    text = text.replace(f"{name}:", "").replace("You:", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return dbc.Card(text, style=style, body=True, color="primary", inverse=True)

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=get_asset_url("bot.png"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")
    

conversation = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse",
    },
)

controls = dbc.InputGroup(
    children=[
        dbc.Input(id="user-input", placeholder="Write to the chatbot...", type="text"),
        dbc.InputGroupText(dbc.Button("Submit", id="submit")),
    ]
)

@callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [
        textbox(x, box="user") if i % 2 == 0 else textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]


@callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""


@callback(
    [Output("store-conversation", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)

def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    if n_clicks == 0 and n_submit is None:
        return "", None

    if user_input is None or user_input == "":
        return chat_history, None

    name = "Jose"

    prompt = dedent(
        f"""
    {description}

    You: Hello {name}!
    {name}: Hello! Glad to be talking to you today.
    """
    )

    # First add the user input to the chat history
    chat_history += f"You: {user_input}<split>{name}:"

    model_input = prompt + chat_history.replace("<split>", "\n")

    response = openai.Completion.create(
        engine="davinci",
        prompt=model_input,
        max_tokens=250,
        stop=["You:"],
        temperature=0.3,
    )
    model_output = response.choices[0].text.strip()

    chat_history += f"{model_output}<split>"

    return chat_history, None


# Función para crear el layout del chatbot
def layout():
    page = html.Div(
        children=[
            header.create_header(),
            create_chat_menu(),
            dcc.Store(id="store-conversation", data=""),
            #create_chat(),
            conversation,
            controls,
            dbc.Spinner(html.Div(id="loading-component")),
        ]
    )
    return page