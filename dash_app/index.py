import os
import sys

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import homepage_layout, dashboard_layout, mv_layout

app.layout = html.Div(children=[dcc.Location(id='url', refresh=False),
                                html.Div(id='page-content')])
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    """
    if pathname == '/':
        return homepage_layout
    elif pathname == '/dashboard':
        return dashboard_layout
    elif pathname == '/market':
        return mv_layout
    else:
        return '404'

if __name__ == '__main__':
    sys.path.append(os.getcwd())
    app.run_server(host='0.0.0.0',
                   port=8050,
                   debug=True)
