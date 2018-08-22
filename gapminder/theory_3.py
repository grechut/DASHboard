
from random import randint

import json

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import options


app = dash.Dash(__name__)
app.title = "Hello advanced Dash"

## State
# "With Great Power Comes Great Responsibility" - Uncle Ben, Spiderman
# app.config["suppress_callback_exceptions"] = True

app.layout = html.Div(
    [
        # html.Button("Plus 1", id="plus_1"),
        # html.Button("Plus 2", id="plus_2"),
        # html.Div(id="shared_state"),
        # # html.Div(id="shared_state", style={"display": "none"})
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


# @app.callback(
#     Output("shared_state", "children"),
#     [Input("plus_1", "n_clicks"), Input("plus_2", "n_clicks")],
#     [State("shared_state", "children")],
# )
# def change_state(plus1_clicks, plus2_clicks, shared_state):
#     if shared_state:
#         shared_state = json.loads(shared_state)
#     else:
#         shared_state = {"value": 0, "plus1_clicks": 0, "plus2_clicks": 0}

#     if plus1_clicks is not None and plus1_clicks - shared_state['plus1_clicks']:
#         shared_state['value'] += 1
#         shared_state['plus1_clicks'] = plus1_clicks
#     elif plus2_clicks is not None and plus2_clicks - shared_state['plus2_clicks']:
#         shared_state['value'] += 2
#         shared_state['plus2_clicks'] = plus2_clicks

#     return json.dumps(shared_state)

## Interval

# app.layout = html.Div(
#     [
#         dcc.Interval(id="some_interval", interval=1000),
#         # html.Div(id="interval_container"),
#         # dcc.Dropdown(
#         #     id="interval_handling_dropdown",
#         #     options=options(["go", "no go"]),
#         #     value="no go",
#         # ),
#         html.H1(id="some_header"),
#     ]
# )


# @app.callback(
#     Output("some_header", "children"), [Input("some_interval", "n_intervals")]
# )
# def print_random_header(n_intervals):
#     return randint(0, 100)


# @app.callback(
#     Output("interval_container", "children"),
#     [Input("interval_handling_dropdown", "value")],
# )
# def control_interval(interval_mode):
#     if interval_mode == "go":
#         return dcc.Interval(id="some_interval", interval=1000)
#     return []


## Caching
# from flask_caching import Cache

# cache = Cache(app.server, config={"CACHE_TYPE": "simple"})


# @cache.memoize(10)
# def get_cached_value(start, stop):
#     return randint(start, stop)


# app.layout = html.Div(
#     [
#         html.H1(get_cached_value(1, 100)),
#         html.H1(get_cached_value(1, 100)),
#         html.H1(get_cached_value(1, 100)),
#         html.H1(get_cached_value(1, 100)),
#         html.H1(get_cached_value(1, 101)),
#     ]
# )

if __name__ == "__main__":
    app.run_server(debug=True)
