import json
from collections import defaultdict

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from flask_caching import Cache

from data import load_data, get_config, get_countires_mapping
from utils import CircleMarkerSizer, options, get_axis


# Loading data
data = load_data()

# Options
DATA_CHOICES = sorted(list(data.keys()))
DEFAULT_X_AXIS = "Life expectancy"
DEFAULT_Y_AXIS = "GDP per capita"
COUNTIRES_MAPPING = get_countires_mapping()
SUPPORTED_COUNTRIES = COUNTIRES_MAPPING.keys()

init_config = get_config(
    data, DEFAULT_X_AXIS, DEFAULT_Y_AXIS, supported_countries=SUPPORTED_COUNTRIES
)

# Creating app
app = dash.Dash(__name__)
app.title = "Poor man's Gapminder"

# Journey begins
app.config["suppress_callback_exceptions"] = True


cache = Cache(app.server, config={"CACHE_TYPE": "simple"})


# TODO Implement cached version of get_config and call it 'get_config_cached'.
#   The one below is NOT CACHED :)
get_config_cached = get_config


# Add Materialize CSS for friendly styling
app.css.append_css(
    {
        "external_url": "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"
    }
)
app.scripts.append_script(
    {
        "external_url": "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js"
    }
)


# Layout
app.layout = html.Div(
    [
        html.Div(
            className="row",
            children=[
                html.H6("Bubbles"),
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="col s12 m6 l6",
                            children=[
                                html.Label("Y Axis"),
                                dcc.Dropdown(
                                    id="y_axis_selection",
                                    options=options(DATA_CHOICES),
                                    value=DEFAULT_Y_AXIS,
                                ),
                            ],
                        ),
                        html.Div(
                            className="col s12 m6 l6",
                            children=[
                                html.Label("Countries"),
                                dcc.Dropdown(
                                    id="countries_selection",
                                    options=options(init_config["countries"]),
                                    value=[],
                                    multi=True,
                                ),
                            ],
                        ),
                    ],
                ),
            ],
            style={"margin": "0 20px"},
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col l9 m9 s9",
                    children=[dcc.Graph(id="main_chart", animate=True)],
                ),
                html.Div(
                    className="col l3 m3 s3", children=[html.Div(id="histograms")]
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="col l3 m6 s6",
                    children=[
                        html.Button("Play", id="play_button", className="btn"),
                        html.Button(
                            "Pause",
                            id="pause_button",
                            className="btn red",
                            style={"margin-left": "20px"},
                        ),
                    ],
                ),
                html.Div(
                    className="col l6 m6 s6",
                    children=[
                        html.Label("X Axis"),
                        dcc.Dropdown(
                            id="x_axis_selection",
                            options=options(DATA_CHOICES),
                            value=DEFAULT_X_AXIS,
                        ),
                    ],
                ),
            ],
            style={"margin": "-20px 0 0 40px"},
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    id="year_slider_container",
                    children=[
                        dcc.Slider(
                            id="year_slider", value=len(init_config["years"]) - 1
                        )
                    ],
                )
            ],
            style={"margin": "0 40px"},
        ),
        html.Div(id="interval_container"),
        html.Div(id="play_state", style={"display": "none"}),
    ]
)


# Callbacks
@app.callback(
    # year_slider_container needed because we need to update multiple properties of slider
    Output("year_slider_container", "children"),
    [
        Input(component_id="x_axis_selection", component_property="value"),
        Input(component_id="y_axis_selection", component_property="value"),
    ],
)
def update_year_slider(x_axis_selection, y_axis_selection):
    if not x_axis_selection or not y_axis_selection:
        return []

    config = get_config_cached(
        data,
        x_axis_selection,
        y_axis_selection,
        supported_countries=SUPPORTED_COUNTRIES,
    )
    years = config["years"]

    marks = {i: year for i, year in enumerate(years)}
    if len(years) > 30:
        marks = {i: year if i % 5 == 0 else "" for i, year in enumerate(years)}

    return [
        html.Label("Year"),
        dcc.Slider(
            id="year_slider",
            min=0,
            max=len(years) - 1,
            value=len(years) - 1,
            marks=marks,
            updatemode="drag",
        ),
    ]


@app.callback(
    Output("main_chart", "figure"),
    [
        Input(component_id="x_axis_selection", component_property="value"),
        Input(component_id="y_axis_selection", component_property="value"),
        Input(component_id="year_slider", component_property="value"),
        Input(component_id="countries_selection", component_property="value"),
    ],
)
def update_chart(x_axis_selection, y_axis_selection, year_idx, countries_selection):
    if not x_axis_selection or not y_axis_selection or year_idx is None:
        return

    config = get_config_cached(
        data,
        x_axis_selection,
        y_axis_selection,
        supported_countries=SUPPORTED_COUNTRIES,
    )

    # one of axis is updated but slider is still not updated
    year_idx = min(len(config["years"]) - 1, year_idx)
    year = config["years"][year_idx]

    marker_sizer = CircleMarkerSizer(config["z_df"][year])

    return {
        "data": [
            go.Scatter(
                x=[config["x_df"].loc[country, year]],
                y=[config["y_df"].loc[country, year]],
                mode="markers+text" if country in countries_selection else "markers",
                textposition="top center",
                text=["{} ({})".format(country, year)],
                marker={
                    "size": marker_sizer.size(config["z_df"].loc[country, year]),
                    # TODO: Add opacity for non-selected countries if there is some country selected.
                    # TODO: Add color corresponding to which part of the world country belongs. Hint: COUNTIRES_MAPPING
                    "line": {"width": 2},
                },
                name="",  # hide trace-39 etc
            )
            for country in config["countries"]
        ],
        "layout": {
            "showlegend": False,
            "xaxis": get_axis(config["x_df"]),
            "yaxis": get_axis(config["y_df"]),
            "height": 500,
            "margin": {"b": 30, "r": 0, "t": 30},
        },
    }


@app.callback(
    Output("histograms", "children"),
    [
        Input(component_id="x_axis_selection", component_property="value"),
        Input(component_id="y_axis_selection", component_property="value"),
        Input(component_id="year_slider", component_property="value"),
    ],
)
def update_hist_chart(x_axis_selection, y_axis_selection, year_idx):
    if not x_axis_selection or not y_axis_selection or year_idx is None:
        return

    config = get_config_cached(
        data,
        x_axis_selection,
        y_axis_selection,
        supported_countries=SUPPORTED_COUNTRIES,
    )

    # one of axis is updated but slider is still not updated
    year_idx = min(len(config["years"]) - 1, year_idx)
    year = config["years"][year_idx]

    return [
        html.Div(
            className="row",
            children=[
                html.Div(
                    dcc.Graph(
                        id="y_hist",
                        figure={
                            "data": [
                                go.Histogram(
                                    x=data[y_axis_selection][year],
                                    nbinsx=10,
                                    opacity=0.5,
                                )
                            ],
                            "layout": {
                                "title": y_axis_selection,
                                "titlefont": {"size": 12},
                                "height": 250,
                                "margin": {"l": 30, "b": 30, "t": 30, "r": 30},
                                "yaxis": {"showticklabels": False},
                            },
                        },
                    )
                ),
                html.Div(
                    dcc.Graph(
                        id="x_hist",
                        figure={
                            "data": [
                                go.Histogram(
                                    x=data[x_axis_selection][year],
                                    nbinsx=10,
                                    opacity=0.5,
                                )
                            ],
                            "layout": {
                                "title": x_axis_selection,
                                "titlefont": {"size": 12},
                                "height": 250,
                                "margin": {"l": 30, "b": 30, "t": 50, "r": 30},
                                "yaxis": {"showticklabels": False},
                            },
                        },
                    )
                ),
            ],
        )
    ]


@app.callback(
    Output("play_state", "children"),
    [
        Input("play_button", "n_clicks"),
        Input("pause_button", "n_clicks"),
        Input("year_slider", "value"),
    ],
    [State("play_state", "children"), State("year_slider", "max")],
)
def player_state(play_clicks, pause_clicks, year_value, current_state, year_max):
    if current_state:
        state_dict = json.loads(current_state)
    else:
        state_dict = {"state": None, "pause": 0, "play": 0}

    if play_clicks is not None and play_clicks - state_dict["play"]:
        state_dict["play"] = play_clicks
        state_dict["state"] = True
    elif pause_clicks is not None and pause_clicks - state_dict["pause"]:
        state_dict["pause"] = pause_clicks
        state_dict["state"] = False
    else:
        if year_value == year_max:
            state_dict["state"] = False
        else:
            return current_state

    return json.dumps(state_dict)


@app.callback(
    Output("interval_container", "children"), [Input("play_state", "children")]
)
def create_interval(play_state):
    if play_state:
        play_state = json.loads(play_state)["state"]
    # TODO When playing is on, return interval with id 'play_interval'
    return []


@app.callback(
    Output("year_slider", "value"),
    [Input("play_interval", "n_intervals")],
    [
        State("play_state", "children"),
        State("year_slider", "value"),
        State("year_slider", "max"),
        State("year_slider", "min"),
    ],
)
def increase_year(n_intervals, play_state, year_value, year_max, year_min):
    if play_state:
        play_state = json.loads(play_state)["state"]

    if year_value == year_max and play_state:
        return year_min

    # TODO When playing is on, return year value increased by 1 year.
    #   Do not increase too much (HINT: year_max).
    return year_value


if __name__ == "__main__":
    app.run_server(debug=True)
