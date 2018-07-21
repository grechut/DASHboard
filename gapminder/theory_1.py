import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app_utils import options


app = dash.Dash(__name__)
app.title = "Hello title"

# Components
app.layout = html.Div(
    [
        html.H1("Hello world"),
        html.H2("How are you?"),
        dcc.Dropdown(
            id="my_first_dropdown",
            options=[
                {"label": "GDP", "value": "gdp"},
                {"label": "Population", "value": "population"},
            ],
            value="gdp",
        ),
        dcc.Dropdown(
            id="my_second_dropdown",
            options=options(["Poland", "Jamaica", "Chile"]),
            value=["Poland"],
            multi=True,
        ),
        dcc.Slider(
            id="year_slider",
            min=0,
            max=3,
            value=0,
            marks={0: "2000", 1: "2001", 2: "2002", 3: "2003"},
        ),
        html.Div(
            id="first_identifiable_div",
            children=[
                html.H1("Here goes graph:"),
                dcc.Graph(
                    id="first_graph",
                    # figure={
                    #     "data": [
                    #         go.Scatter(
                    #             x=[10, 20, 30], y=[20, 40, 100], name="super_line"
                    #         ),
                    #         # go.Bar(x=[10, 20], y=[40, 10], name="super_bar"),
                    #     ],
                    #     # "layout": {"title": "hello from graph", "height": 500},
                    # },
                ),
            ],
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
