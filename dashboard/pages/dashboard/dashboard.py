import dash
import pages.dashboard.header as header
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html

dash.register_page(
    __name__,
    path="/",
    title="Dashboard Analytics",
    name="Dashboard Analytics",
    description="A Demo Dashboard for Sale",
)

data = (
    pd.read_csv("./data/data.csv")
    .assign(Date=lambda data: pd.to_datetime(data["PODate"], format="%m/%d/%Y"))
    .sort_values(by="Date")
)

vendor_name = data["VendorName"].sort_values().unique()
cust_number = data["cust_number"].sort_values().unique()


def layout():
    page = html.Div(
        children=[
            header.create_header(),
            create_menu(),
            create_charts(),
        ]
    )
    return page


# Función para crear el menú de filtros
def create_menu():
    vendor_options = [{"label": "All", "value": "All"}] + [
        {"label": vendor, "value": vendor} for vendor in vendor_name
    ]
    customer_options = [{"label": "All", "value": "All"}] + [
        {"label": customer, "value": customer} for customer in cust_number
    ]
    menu = html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(children="Customer", className="menu-title"),
                    dcc.Dropdown(
                        id="customer-filter",
                        options=customer_options,
                        value="All",
                        clearable=False,
                        className="dropdown",
                    ),
                ]
            ),
            html.Div(
                children=[
                    html.Div(children="Vendor Name", className="menu-title"),
                    dcc.Dropdown(
                        id="vendor-filter",
                        options=vendor_options,
                        value=vendor_name[0],
                        clearable=False,
                        searchable=True,
                        className="dropdown",
                    ),
                ],
            ),
            html.Div(
                children=[
                    html.Div(children="Date Range", className="menu-title"),
                    dcc.DatePickerRange(
                        id="date-range",
                        min_date_allowed=data["Date"].min().date(),
                        max_date_allowed=data["Date"].max().date(),
                        start_date=data["Date"].min().date(),
                        end_date=data["Date"].max().date(),
                    ),
                ]
            ),
        ],
        className="dashboard-menu",
    )
    return menu


# Función para crear las gráficas
def create_charts():
    charts = html.Div(
        children=[
            # Gráficas horizontales
            html.Div(
                children=[
                    dcc.Graph(
                        id="sales-chart",
                        config={"displayModeBar": False},
                    ),
                ],
                className="card",
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="quantity-chart",
                        config={"displayModeBar": False},
                    ),
                ],
                className="card",
            ),
        ],
        className="wrapper",
    )
    return charts


@callback(
    Output("customer-filter", "options"),
    Input("vendor-filter", "value"),
)
def update_customer_options(vendor):
    if vendor == "All":
        # Si se selecciona "All", mostrar todos los usuarios
        user_options = [{"label": "All", "value": "All"}] + [
            {"label": customer, "value": customer} for customer in cust_number
        ]
    else:
        # Mostrar solo los usuarios asociados al proveedor seleccionado
        customer_for_vendor = data[data["VendorName"] == vendor]["cust_number"].unique()
        customer_options = [{"label": "All", "value": "All"}] + [
            {"label": customer, "value": customer} for customer in customer_for_vendor
        ]

    return customer_options


@callback(
    Output("sales-chart", "figure"),
    Output("quantity-chart", "figure"),
    Input("customer-filter", "value"),
    Input("vendor-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(customer, vendor, start_date, end_date):
    # Aplicar filtros según los valores seleccionados
    if vendor != "All":
        filtered_data = data[data["VendorName"] == vendor]
    else:
        filtered_data = data

    if customer != "All":
        filtered_data = filtered_data[filtered_data["cust_number"] == customer]

    filtered_data = filtered_data[
        (filtered_data["Date"] >= start_date) & (filtered_data["Date"] <= end_date)
    ]

    sales_chart_figure = px.scatter(
        filtered_data,
        x="Date",
        y="PurchasePrice",
        labels={"Date": "Date", "PurchasePrice": "Price"},
        title="Purchase Price",
    )
    sales_chart_figure.update_layout(template="plotly_white")

    quantity_chart_figure = px.scatter(
        filtered_data,
        x="Date",
        y="Quantity",
        labels={"Date": "Date", "Quantity": "Quantity"},
        title="Quantity",
    )
    quantity_chart_figure.update_layout(template="plotly_white")

    return sales_chart_figure, quantity_chart_figure
