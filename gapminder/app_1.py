import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from data import load_data, get_config, get_countires_mapping
from app_utils import options


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


# Add Materialize CSS for friendly styling
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
                            #     Add here chart like in "Plotly" chapter.
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
                        # TODO:
                        #     Create dropdown that handles selection for x axis.
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
                        dcc.Slider(id="year_slider")
                        # TODO:
                        #     Add slider min, max, labels, value
                    ],
                )
            ],
            style={"margin": "0 40px"},
        ),
    ]
)

# TODO Ask questions about places you do not 100% get. Be direct ;)


if __name__ == "__main__":
    app.run_server(debug=True)
