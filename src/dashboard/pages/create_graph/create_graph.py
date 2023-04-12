"""Graph display module.

This module displays different types of graphs based on input,
from either a csv-file or from a database.
"""
import base64
import io

import dash
from dash import callback, dcc, html
from dash.dependencies import Component, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import polars as pl

from dashboard.components import button, icon

dash.register_page(__name__, path="/create-graph", nav_item=False)


# sets the colors of the login page
colors = {
    "background": "#E9E9F2",
    "text": "#7FDBFF",
    "meny_back": "#636AF2",
    "white": "#FFFFFF",
    "dark_purp": "#2F3273",
    "black": "#00000",
    "temp": "#ffc0cb",
}

event = {"event": "click", "props": ["scatter", "line"]}


# the main graphical component for the entire csv graph create page page
def layout() -> Component:
    """Main layout component that is parent to all other components.

    Returns:
        A html.div component with all other components.
    """
    # main background element
    return html.Div(
        className=f'bg-[{colors["background"]}] flex h-screen',
        children=[graph_window(), right_settings_bar()],
    )


def csv_button() -> Component:
    """Button to upload a csv file.

    Returns:
        A dcc.upload containg a csv-file.
    """
    return dcc.Upload(
        className=f"bg-[{colors['meny_back']}] duration-150 shrink flex flex-col "
        "cursor-pointer p-3 mr-2 rounded-md hover:bg-[#2F3273]",
        id="uploaded_data",
        children=html.Div(
            className="flex items-center",
            children=[
                icon("upload", size=36, className="mr-1"),
                html.P(className="whitespace-nowrap", children="CSV-file"),
            ],
        ),
        # false so multiple files cant be uploaded
        multiple=False,
    )


def graph_window() -> Component:
    """A window used to display the created graph.

    Returns:
        A html.div containing the created graph.
    """
    return html.Div(
        className="bg-white w-full ml-[3rem] my-[3rem] rounded-md shadow-md",
        children=html.Div(id="graph_output"),
    )


def display_graph(df: pl.DataFrame, graph_type: str) -> Component:
    """Displays a graph based in the chosen type by the user.

    Args:
        df: a dataframe containg used for creating the graph.
        graph_type: a string used to check what type of graph
        to draw.
    """
    if df is not None:
        if graph_type == "scatter":
            fig = px.scatter(
                df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file"
            )
        if graph_type == "line":
            fig = px.line(df, x=list(df["x"]), y=list(df["y"]), title="Test graph from csv file")
        if graph_type == "histo":
            fig = px.histogram(df, x=list(df["x"]), title="Test graph from csv file")
        return dcc.Graph(className="m-5 shadow-md", figure=fig)


def top_right_settings() -> html.Div:
    """Buttons for the graph settings.

    Returns:
        html.Div: A div containing the buttons used for graph settings
    """
    # Container
    return html.Div(
        className="flex flex-col space-y-4",
        children=[
            html.Div(
                className="flex items-center",
                children=[
                    icon("settings", fill=1, size=36),
                    html.H1(
                        className="text-[1.5rem] w-full text-center", children="Customize graph"
                    ),
                ],
            ),
            upload_buttons(),
            radio_buttons(),
        ],
    )


def upload_buttons() -> html.Div:
    """Buttons for uploading file.

    Returns:
        html.Div: Div with upload buttons with either CSV or database
    """
    return html.Div(
        className="flex flex-col",
        children=[
            html.P("Upload data"),
            html.Div(
                className="flex text-white",
                children=[
                    csv_button(),
                    button(
                        "database",
                        "Database",
                        size=18,
                        className="bg-[#636af2] hover:bg-[#2F3273] justify-center flex-1",
                    ),
                ],
            ),
        ],
    )


def radio_buttons() -> html.Div:
    """Radio buttons for the graph type.

    Returns:
        html.Div: Div with radio buttons
    """
    return html.Div(
        className="flex flex-col",
        children=[
            html.P("Plot type "),
            dcc.RadioItems(
                className="flex space-x-2",
                options=[
                    radio_item("Line", "line", "show_chart"),
                    radio_item("Bar", "histo", "bar_chart"),
                    radio_item("Scatter", "scatter", "scatter_plot"),
                ],
                inputClassName="peer hidden",
                value="line",
                labelStyle={"": ""},
                labelClassName="flex-1",
                id="choose_graph_type",
            ),
        ],
    )


def right_settings_bar() -> Component:
    """Right settings bar.

    Returns:
        A html.div containing all the settings components.
    """
    return html.Div(
        className="bg-white flex flex-col m-[3rem] p-[2rem] shadow-md rounded-lg",
        children=[
            top_right_settings(),
            # Lower part of the settings bar
            html.Div(
                className="flex mt-auto justify-center space-x-2 text-white",
                children=[
                    button(
                        "cancel",
                        "Cancel",
                        size=18,
                        id="cancel-graph",
                        className="bg-[#636af2] px-5 hover:bg-[#2F3273]",
                    ),
                    button(
                        "check",
                        "Create dashboard",
                        size=18,
                        id="create-graph",
                        className="bg-[#636af2] px-5 py-3 hover:bg-[#2F3273]",
                    ),
                ],
            ),
        ],
    )


def radio_item(name: str, value: str, icon_name: str) -> dict[str, html.Div]:
    """Creates a styled radio button.

    Args:
        name (str): Text that the radio should display
        value (str): checked value
        icon_name (str): name of the icon
    Returns:
        dict[str, html.Div]: Dictionary containing label and
        values required for dcc.RadioItems
    """
    classname = (
        "peer-checked:opacity-100 peer-checked:shadow-lg peer-checked:bg-[#03c04a] "
        "peer-checked:text-[#2f3273] flex flex-col items-center p-3 cursor-pointer "
        "bg-[#636af2] rounded-md shadow-md duration-150 hover:bg-[#2F3273] text-white"
    )
    return {
        "label": [
            html.Div(className=classname, children=[icon(icon_name, size=40), html.P(name)]),
        ],
        "value": value,
    }


def parse_contents(contents: str, filename: str) -> pl.DataFrame:
    """Parses the input from a csv-file.

    Args:
        contents: the csv-file content.
        filename: the csv-file name.

    Returns:
        A parsed and read version of the csv-file.
    """
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    return pl.read_csv(io.StringIO(decoded.decode("utf-8")))


@callback(
    Output("graph_output", "children"),
    Input("uploaded_data", "contents"),
    State("uploaded_data", "filename"),
    Input("choose_graph_type", "value"),
)
def update_output(content: str, filename: str, value: str) -> Component:
    """Update_output takes input creates graph from a dataframe.

    Args:
        content: csv-file content.
        filename: csv-file name.
        value: chosen graph type (linear, scatter etc.).

    Returns:
        A graph in the form of a plotly figure.
    """
    if content is None:
        raise PreventUpdate

    try:
        df = parse_contents(content, filename)
    except ValueError:
        raise PreventUpdate

    loc_graph = display_graph(df, value)
    return loc_graph
