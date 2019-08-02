import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Output, Input, State

from app import app
# will be used for callbacks

# define DOM components
# navbar = html.Div()
# row_1 =
# row_2 =

# assemble components into layout
layout_ = []

# define callbacks
@app.callback(Output(component_id="", component_property=""),
              [Input(component_id="input-widget", component_property="input_widget_value")])
def responsive_widget_1(input_widget_value):
    """
    """
    pass
