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
        dcc.Dropdown(
            id="x_axis_selection", options=[{"label": k, "value": k} for k in data_keys]
        ),
        dcc.Dropdown(
            id="y_axis_selection", options=[{"label": k, "value": k} for k in data_keys]
        ),
        dcc.Graph(id="main_chart"),
    ]
)


@app.callback(
    Output("main_chart", "figure"),
    [
        Input(component_id="x_axis_selection", component_property="value"),
        Input(component_id="y_axis_selection", component_property="value"),
    ],
)
def update_chart(x_axis_selection, y_axis_selection, year=2005):
    year = str(year)

    return {
        "data": [
            go.Scatter(
                x=data[x_axis_selection][year],
                y=data[y_axis_selection][year],
                mode="markers+text",
                text=data[x_axis_selection][year].index,
            )
        ]
    }


if __name__ == "__main__":
    app.run_server(debug=True)

