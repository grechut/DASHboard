"""
- play/pause interval
- size of bubble => dropdown selection
- color of bubble => color of continent
- map of the world => legend for color continents

- multi choice of countires
- selected countries get label
- search for countries

- make size value more dynamic (not population only)

- color hue

- how to properly keep state?
    how to propagate state so that we do not have callback hell?

- make it look better
"""

import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

from data import load_data


TITLE = "Poor man's Gapminder"
TOTAL_POPULATION = "Total population"

# Loading data
data = load_data()
data_keys = list(data.keys())

population_df = data[TOTAL_POPULATION]

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
                html.H1("Bubbles"),
                html.Label("Year"),
                html.Div([dcc.Slider(id="year_slider")], id="year_slider_container"),
                html.Div(
                    children=[
                        html.Label("Y Axis"),
                        dcc.Dropdown(
                            id="y_axis_selection",
                            options=[{"label": k, "value": k} for k in data_keys],
                            value=data_keys[2],
                        ),
                    ],
                    style={"width": "400px"},
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
                    options=[{"label": k, "value": k} for k in data_keys],
                    value=data_keys[1],
                ),
            ],
            style={"width": "400px"},
        ),
    ]
)


# Callbacks
@app.callback(
    Output("year_slider_container", "children"),
    [
        Input(component_id="x_axis_selection", component_property="value"),
        Input(component_id="y_axis_selection", component_property="value"),
    ],
)
def update_year_slider(x_axis_selection, y_axis_selection):
    if not x_axis_selection or not y_axis_selection:
        return []

    x_years = [int(c) for c in data[x_axis_selection]]
    y_years = [int(c) for c in data[y_axis_selection]]

    min_value = max([x_years[0], y_years[0]])
    max_value = min([x_years[-1], y_years[-1]])

    return (
        dcc.Slider(id="year_slider", min=min_value, max=max_value, value=max_value),
    )


@app.callback(
    Output("main_chart", "figure"),
    [
        Input(component_id="x_axis_selection", component_property="value"),
        Input(component_id="y_axis_selection", component_property="value"),
        Input(component_id="year_slider", component_property="value"),
    ],
)
def update_chart(x_axis_selection, y_axis_selection, year):
    if not x_axis_selection or not y_axis_selection or not year:
        return

    year = str(year)
    marker_size = MarkerSize(population_df[year])

    return {
        "data": [
            go.Scatter(
                x=[data[x_axis_selection].loc[idx, year]],
                y=[data[y_axis_selection].loc[idx, year]],
                mode="markers",  # "markers+text" for labels
                textposition="top right",
                text=[idx],
                # Is it okay to just log or do we need to scale?
                marker={"size": marker_size.size(row[year])},
                name="",  # hide trace-39 etc
            )
            for idx, row in population_df.iterrows()
            if idx in data[x_axis_selection].index
            and idx in data[y_axis_selection].index
        ],
        "layout": {"title": year, "showlegend": False},
    }


# Utils

# Very much POC, rethink.
# Prolly we need log as it will display more fair
class MarkerSize:
    def __init__(self, values, max_size=30):
        self.min_val = values.min()
        self.max_val = values.max()
        self.max_size = max_size

    def size(self, value):
        scaled = (value - self.min_val) / self.max_val
        return scaled * self.max_size


if __name__ == "__main__":
    app.run_server(debug=True)
