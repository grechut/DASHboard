"""
- year slider FIX MEEE
- play/pause interval
- size of bubble => dropdown selection
- color of bubble => color of continent
- map of the world => legend for color continents

- multi choice of countires
- selected countries get label
- search for countries

- color hue

- make it look better
"""

import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from data import load_data


data = load_data()
data_keys = list(data.keys())

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Bubbles"),
        html.Label("X Axis"),
        dcc.Dropdown(
            id="x_axis_selection",
            options=[{"label": k, "value": k} for k in data_keys],
            value=data_keys[0],
        ),
        html.Label("Y Axis"),
        dcc.Dropdown(
            id="y_axis_selection",
            options=[{"label": k, "value": k} for k in data_keys],
            value=data_keys[1],
        ),
        html.Label("Year"),
        html.Div([dcc.Slider(id="year_slider")], id="year_slider_container"),
        dcc.Graph(id="main_chart"),
    ]
)


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

    min_value = max([data[x_axis_selection].min(), data[y_axis_selection].min()])
    max_value = min([data[x_axis_selection].max(), data[y_axis_selection].max()])

    return (
        dcc.Slider(
            id="year_slider",
            min=min_value,
            max=max_value,
            # step=1,
            value=max_value,
            marks={year: str(year) for year in range(min_value, max_value + 1)},
        ),
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

    return {
        "data": [
            go.Scatter(
                x=data[x_axis_selection][year],
                y=data[y_axis_selection][year],
                mode="markers+text",
                text=data[x_axis_selection][year].index,
            )
        ],
        "layout": {"title": year},
    }


if __name__ == "__main__":
    app.run_server(debug=True)
