
from random import randint

import json

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app_utils import options


app = dash.Dash(__name__)
app.title = "Hello advanced Dash"


# * Shared state
# * Simple Interval case
# * Button + clicks (and link to Dash forum confirming that we are not crazy)

# * Heavier customisation of chart (colour, size, opacity, text)
#     * Log axis?
#     * Animate
# * Explain cache


app.layout = html.Div(
    [
        html.Button("Plus 1", id="plus_1"),
        html.Button("Plus 2", id="plus_2"),
        html.Div(id="shared_state")
        # html.Div(id="shared_state", style={"display": "none"})
    ]
)


# @app.callback(
#     Output("shared_state", "children"),
#     [Input("plus_1", "n_clicks")],
#     [State("shared_state", "children")],
# )
# def change_state(plus1_clicked, shared_state):
#     if shared_state:
#         shared_state = json.loads(shared_state)
#     else:
#         shared_state = {"value": 0}

#     if plus1_clicked is not None:
#         shared_state["value"] += 1
#     return json.dumps(shared_state)


# @app.callback(
#     Output("shared_state", "children"),
#     [Input("plus_1", "n_clicks"), Input("plus_2", "n_clicks")],
#     [State("shared_state", "children")],
# )
# def change_state(plus1_clicked, plus2_clicked, shared_state):
#     if shared_state:
#         shared_state = json.loads(shared_state)
#     else:
#         shared_state = {"value": 0}

#     # which one is clicked?
#     if plus1_clicked is not None or plus2_clicked is not None:
#         shared_state["value"] += 1
#     return json.dumps(shared_state)


@app.callback(
    Output("shared_state", "children"),
    [Input("plus_1", "n_clicks"), Input("plus_2", "n_clicks")],
    [State("shared_state", "children")],
)
def change_state(plus1_clicks, plus2_clicks, shared_state):
    if shared_state:
        shared_state = json.loads(shared_state)
    else:
        shared_state = {"value": 0, "plus1_clicks": 0, "plus2_clicks": 0}

    if plus1_clicks is not None and plus1_clicks - shared_state['plus1_clicks']:
        shared_state['value'] += 1
        shared_state['plus1_clicks'] = plus1_clicks
    elif plus2_clicks is not None and plus2_clicks - shared_state['plus2_clicks']:
        shared_state['value'] += 2
        shared_state['plus2_clicks'] = plus2_clicks

    return json.dumps(shared_state)


if __name__ == "__main__":
    app.run_server(debug=True)
