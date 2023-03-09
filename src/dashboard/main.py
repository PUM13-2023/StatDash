import dash
from dash import Dash, html
from dash.dependencies import Component
from flask import Flask

external_scripts = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]

server = Flask(__name__)
app = Dash(__name__, server=server, use_pages=True, external_scripts=external_scripts)


def page_container() -> Component:
    return html.Div([html.H1("PUM13-2023"), dash.page_container])


app.layout = page_container

if __name__ == "__main__":
    app.run("127.0.0.1", "8000")
