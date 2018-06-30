"""
- bubble size mathematically correct

- set properly height/width

- better state management
    - how to properly keep state?
    - how to propagate state so that we do not have callback hell?

- play/pause interval

- add 2nd chart, e.g. with distributions


Optional:
- color hue
- color of bubble => color of continent
- more than population for bubble size
- present dots from previously selected year

- map of the world => legend for color continents

Other quesitons:
- how to deal with dynamic data and selections?
- what is order of callbacks doing?
"""

import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

from data import (
    load_data,
    prepare_data,
)
from app_utils import MarkerSize, options, get_axis


TITLE = "Poor man's Gapminder"
TOTAL_POPULATION = "Total population"

# Loading data
data = load_data()
DATA_CHOICES = list(data.keys())

DEFAULT_X_AXIS = DATA_CHOICES[1]
DEFAULT_Y_AXIS = DATA_CHOICES[2]

config = prepare_data(
    data, DEFAULT_X_AXIS, DEFAULT_Y_AXIS,
)


# Creating app
app = dash.Dash(__name__)
app.title = TITLE


# Materialize, not sure what to use
external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"
]
for css in external_css:
    app.css.append_css({"external_url": css})
external_js = [
    "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js"
]
for js in external_js:
    app.scripts.append_script({"external_url": js})


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
                            className="col l12",
                            children=[dcc.Slider(id="year_slider")],
                            id="year_slider_container",
                        ),
                    ]
                ),
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
                                    options=options(config['countries']),
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
        html.Div(className="row", children=[dcc.Graph(id="main_chart")]),
        html.Div(
            className="row",
            children=[
                html.Label("X Axis"),
                dcc.Dropdown(
                    id="x_axis_selection",
                    options=options(DATA_CHOICES),
                    value=DEFAULT_X_AXIS,
                ),
            ],
            style={"width": "300px"},
        ),
    ]
)


# Callbacks
@app.callback(
    # year_slider_container needed because we need to update multiple properties of slider
    Output("year_slider_container", "children"),
    [
        Input(component_id="x_axis_selection", component_property="value"),
        Input(component_id="y_axis_selection", component_property="value"),
        Input(component_id="countries_selection", component_property="value"),
    ],
)
def update_year_slider(x_axis_selection, y_axis_selection, countries_selection):
    if not x_axis_selection or not y_axis_selection:
        return []

    config = prepare_data(
        data, x_axis_selection, y_axis_selection, countries_selection,
    )
    years = config['years']

    marks = {i: year for i, year in enumerate(years)}
    if len(years) > 30:
        marks = {i: year if i % 5 == 0 else '' for i, year in enumerate(years)}

    return [
        html.Label("Year"),
        dcc.Slider(
            id="year_slider",
            min=0,
            max=len(years)-1,
            value=len(years)-1,
            marks=marks,
            updatemode="drag",
            dots=False,
        ),
    ]


@app.callback(
    Output("main_chart", "figure"),
    [
        Input(component_id="x_axis_selection", component_property="value"),
        Input(component_id="y_axis_selection", component_property="value"),
        # Workaround for proper detection of callback dependencies
        Input(component_id="year_slider_container", component_property="children"),
        Input(component_id="year_slider", component_property="value"),
        Input(component_id="countries_selection", component_property="value"),
    ],
)
def update_chart(
    x_axis_selection, y_axis_selection, year_container, year,
    countries_selection,
):
    if not x_axis_selection or not y_axis_selection or not year:
        return

    config = prepare_data(
        data, x_axis_selection, y_axis_selection, countries_selection,
    )
    selected_year = config['years'][year]

    marker_size = MarkerSize(config['z_df'][selected_year])
    return {
        "data": [
            go.Scatter(
                x=[config['x_df'].loc[country, selected_year]],
                y=[config['y_df'].loc[country, selected_year]],
                mode="markers+text" if countries_selection else "markers",
                textposition="top center" if countries_selection else None,
                text=[country],
                # Is it okay to just log or do we need to scale?
                marker={
                    "size": marker_size.size(
                        config['z_df'].loc[country, selected_year]
                    )
                },
                name="",  # hide trace-39 etc
            )
            for country in config['countries']
        ],
        "layout": {
            "title": selected_year,
            "showlegend": False,
            "xaxis": get_axis(config['x_df']),
            "yaxis": get_axis(config['y_df']),
            "height": "600px",
        },
    }


if __name__ == "__main__":
    app.run_server(debug=True)
