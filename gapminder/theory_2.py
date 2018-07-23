import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app_utils import options


app = dash.Dash(__name__)
app.title = "Hello callbacks"

# Layout
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="my_first_dropdown",
            options=[
                {"label": "GDP", "value": "gdp"},
                {"label": "Population", "value": "population"},
            ],
            value="gdp",
        ),
        html.H1(id="dropdown_value"),
    ]
)


@app.callback(
    Output("dropdown_value", "children"), [Input("my_first_dropdown", "value")]
)
def update_h1(dropdown_value):
    return dropdown_value


if __name__ == "__main__":

    app.run_server(debug=True)
