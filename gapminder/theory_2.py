from random import randint

import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from app_utils import options


app = dash.Dash(__name__)
app.title = "Hello callbacks"


app.layout = html.Div(
    [
        # dcc.Dropdown(
        #     id="my_first_dropdown", options=options(["gdp", "population"]), value="gdp"
        # ),
        # # html.H1(id="dropdown_value"),
        # # # dcc.Dropdown(
        # # #     id="my_second_dropdown",
        # # #     options=options(["Poland", "Not Poland"]),
        # # #     value="Poland",
        # # # ),
        # # # # html.Div(id="fully_new_element_container"),
        # # # # # When you want to dynamically update component that later affects other components
        # # # # # html.Div(id="slider_container", children=[dcc.Slider(id="super_slider")]),
        # # # # # # html.Div(id="slider_affected_part"),
    ]
)


# # @app.callback(
# #     Output("dropdown_value", "children"), [Input("my_first_dropdown", "value")]
# # )
# def update_h1(dropdown_value):
#     return dropdown_value


# @app.callback(
#     Output("fully_new_element_container", "children"),
#     [Input("my_first_dropdown", "value")],
#     [State("my_second_dropdown", "value")],
# )
# def update_container(first_dropdown_value, second_dropdown_value):
#     return [
#         # dcc.Graph(
#         #     id="new_graph",
#         #     figure={
#         #         "data": [
#         #             go.Bar(x=[first_dropdown_value, second_dropdown_value], y=[10, 11])
#         #         ]
#         #     },
#         # ),
#         # # html.H5("Hello from H5"),
#     ]


# @app.callback(
#     Output("slider_container", "children"), [Input("my_first_dropdown", "value")]
# )
# def update_slider_container(dropdown_value):
#     return dcc.Slider(id="super_slider", min=0, max=10, value=randint(0, 10))


# # @app.callback(
# #     Output("slider_affected_part", "children"), [Input("super_slider", "value")]
# # )
# # def update_slider_affected_part(slider_value):
# #     return html.H1(f"Slider value: {slider_value}")


if __name__ == "__main__":
    app.run_server(debug=True)
