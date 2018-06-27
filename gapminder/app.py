"""
- better state management
    - how to do first render?
    - how to properly keep state?
    - how to propagate state so that we do not have callback hell?

- play/pause interval

- make size value more dynamic (not population only)


Optional:
- color hue
- color of bubble => color of continent
- map of the world => legend for color continents

Other quesitons:
- how to deal with dynamic data and selections?

"""

import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

from data import load_data
from app_utils import MarkerSize, options


TITLE = "Poor man's Gapminder"
TOTAL_POPULATION = "Total population"

# Loading data
data = load_data()
DATA_CHOICES = list(data.keys())

population_df = data[TOTAL_POPULATION]
COUNTRIES = list(population_df.index)

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
                    className="row",
                    children=[
                        html.Div(
                            className="col s12 m6 l6",
                            children=[
                                html.Label("Y Axis"),
                                dcc.Dropdown(
                                    id="y_axis_selection",
                                    options=options(DATA_CHOICES),
                                    value=DATA_CHOICES[2],
                                ),
                            ],
                        ),
                        html.Div(
                            className="col s12 m6 l6",
                            children=[
                                html.Label("Countries"),
                                dcc.Dropdown(
                                    id="countries_selection",
                                    options=options(COUNTRIES),
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
                    value=DATA_CHOICES[1],
                ),
            ],
            style={"width": "300px"},
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
        Input(component_id="countries_selection", component_property="value"),
    ],
)
def update_chart(x_axis_selection, y_axis_selection, year, countries_selection):
    if not x_axis_selection or not y_axis_selection or not year:
        return

    countries = countries_selection or COUNTRIES
    year = str(year)

    marker_size = MarkerSize(population_df[year])

    return {
        "data": [
            go.Scatter(
                x=[data[x_axis_selection].loc[country, year]],
                y=[data[y_axis_selection].loc[country, year]],
                mode="markers+text" if countries_selection else "markers",
                textposition="top center" if countries_selection else None,
                text=[country],
                # Is it okay to just log or do we need to scale?
                marker={"size": marker_size.size(population_df.loc[country, year])},
                name="",  # hide trace-39 etc
            )
            for country in countries
            if country in data[x_axis_selection].index
            and country in data[y_axis_selection].index
        ],
        "layout": {"title": year, "showlegend": False},
    }


if __name__ == "__main__":
    app.run_server(debug=True)
