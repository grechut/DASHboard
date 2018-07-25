
from random import randint

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app_utils import options


app = dash.Dash(__name__)
app.title = "Hello advanced Dash"


# * Heavier customisation of chart (colour, size, opacity, text)
#     * Log axis?
#     * Animate
# * Button + clicks (and link to Dash forum confirming that we are not crazy)
# * Simple Interval case
# * Shared state
# * Explain cache


app.layout = html.Div([])


if __name__ == "__main__":
    app.run_server(debug=True)
