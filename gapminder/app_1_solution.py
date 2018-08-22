import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from data import load_data, get_config, get_countires_mapping
from utils import options


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
YEARS = init_config["years"]

# Creating app
app = dash.Dash(__name__)
app.title = "Poor man's Gapminder"


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
                    className="col l12 m12 s12",
                    children=[
                        dcc.Graph(
                            id="main_chart",
                            # TODO:
                            #     Add here chart like in "First Graphs" exercise.
                            figure={
                                "data": [
                                    go.Scatter(
                                        x=[init_config["x_df"].loc[country, YEARS[-1]]],
                                        y=[init_config["y_df"].loc[country, YEARS[-1]]],
                                        mode="markers",
                                        text=[f"{country} ({YEARS[-1]})"],
                                        name="",
                                    )
                                    # for loop to have different colour for each country
                                    for country in init_config["countries"]
                                ],
                                "layout": {
                                    "title": "Gapminder",
                                    "height": 500,
                                    "showlegend": False,
                                },
                            },
                        )
                    ],
                )
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
                            id="year_slider",
                            # TODO:
                            #     Set min, max, marks, value for slider using init_config
                            min=0,
                            max=len(YEARS) - 1,
                            value=len(YEARS) - 1,
                            marks={
                                i: year if i % 5 == 0 else ""
                                for i, year in enumerate(YEARS)
                            },
                        )
                    ],
                )
            ],
            style={"margin": "0 40px"},
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
