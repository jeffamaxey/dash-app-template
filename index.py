import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from pages import homepage_layout, dashboard_layout

app.layout = html.Div(children=[dcc.Location(id='url', refresh=False),
                                html.Div(id='page-content')
                                ])
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    """
    if pathname == 'homepage':
        return homepage.layout
    elif pathname == 'dashboard':
        return dashboard.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',
                   port=8050,
                   debug=True)
