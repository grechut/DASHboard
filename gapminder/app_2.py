import json
from collections import defaultdict

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from data import load_data, get_config, get_countires_mapping
from app_utils import CircleMarkerSizer, options, get_axis


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
                    className="col l9 m9 s9", children=[dcc.Graph(id="main_chart")]
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
                    className="col l6 m6 s6",
                    children=[
                        html.Label("X Axis"),
                        dcc.Dropdown(
                            id="x_axis_selection",
                            options=options(DATA_CHOICES),
                            value=DEFAULT_X_AXIS,
                        ),
                    ],
                )
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
    ]
)


# TODO:
# Output: year slider container (year_slider_container)
# Inputs:
# x axis (x_axis_selection)
# y axis (y_axis_selection)

# @app.callback(
#     # year_slider_container needed because we need to update multiple properties of slider
#     Output("year_slider_container", "children"),
#     [
#         Input(component_id="x_axis_selection", component_property="value"),
#         Input(component_id="y_axis_selection", component_property="value"),
#     ],
# )
def update_year_slider():
    if not x_axis_selection or not y_axis_selection:
        return []

    config = get_config(
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
        # TODO: return slider with properly set properties (id, min, max, value, marks)
    ]


# TODO
# Add Output to main_chart
# Add inputs:
# x_axis (x_axis_selection)
# y_axis (y_axis_selection)

# @app.callback(
#     [
#         Input(component_id="year_slider", component_property="value"),
#     ],
# )
def update_chart():
    if not x_axis_selection or not y_axis_selection or year_idx is None:
        return

    config = get_config(
        data,
        x_axis_selection,
        y_axis_selection,
        supported_countries=SUPPORTED_COUNTRIES,
    )
    year = config["years"][year_idx]

    return {
        "data": [
            go.Scatter(
                x=[config["x_df"].loc[country, year]],
                y=[config["y_df"].loc[country, year]],
                mode="markers",
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

    config = get_config(
        data,
        x_axis_selection,
        y_axis_selection,
        supported_countries=SUPPORTED_COUNTRIES,
    )
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
                # TODO:
                # Implement histogram for x-axis
            ],
        )
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
