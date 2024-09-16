from collections import OrderedDict

import dash
from dash import dcc, html
import plotly.express as px

from dashboard.components.icon import icon

dash.register_page(__name__, path_template="/dashboard/<dashboard_id>")

# Ordered dict containing the name of the button and its corresponding icon name
# Find the icon names here https://fonts.google.com/icons?icon.set=Material+Symbols
buttons = OrderedDict(
    [("Presentation view", "present_to_all"), ("Share", "share"), ("Add graph", "add")]
)


def add_buttons(button_names: OrderedDict[str, str]) -> list[html.Button]:
    buttons: list[html.Button] = []

    for name, icon_ in button_names.items():
        buttons.append(
            html.Button(
                className="flex bg-white items-center mx-2 p-2 rounded-lg "
                          "drop-shadow-sm transition ease-in-out " 
                          "hover:text-white hover:bg-[#777df2] ",
                children=[icon(icon_, className="mr-2"), html.P(name)],
            )
        )

    return buttons


def add_graph_button():
    return(
        html.Button(
            className="flex flex-col text-black/60 duration-[300] hover:rounded-xl "
                      "hover:shadow-md hover:text-black text-3xl justify-center "
                      "transition-all bg-white/70 hover:bg-white shadow-sm h-[25rem] rounded-md w-full ",
            children=[
                html.P(className="mb-3", children="Add new graph"),
                icon( "add_circle", className="text-4xl")
            ]
        )
    )
    


def layout(dashboard_id=None):
    dashboard_name = f"Dashboard {dashboard_id}"

    """
    TODO
        Use the dashboard_id to query
        information from the database about that specific dashboard
    """

    return html.Div(
        className="flex flex-col",
        children=[
            html.Div(
                className="flex p-5 items-center",
                children=[
                    html.H1(className="text-3xl", children=[dashboard_name]),
                    html.Div(className="flex ml-auto", children=add_buttons(buttons)),
                ],
            ),
            html.Div(
                className="flex flex-col px-[5rem] pb-[5rem] items-center",
                # Put a list of the given dashboard's graphs here
                children=[add_graph_button()]
            ),
        ],
    )
