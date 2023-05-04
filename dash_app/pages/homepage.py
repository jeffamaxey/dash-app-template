import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from pages.components import header

body = html.Div(
    children=[html.H3('Homepage'),
              dcc.Dropdown(id='app-1-dropdown',
                           options=[{
                               'label': 'App 1 - {}'.format(i), 'value': i} for i in ['NYC', 'MTL', 'LA']]),
              html.Div(id='app-1-display-value'),
              dcc.Link('Go to Dashboard', href='/pages/dashboard')
              ],
    style={'fontFamily': 'Inconsolata'},
    )

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div("One of two columns"), width=4),
                dbc.Col(html.Div("One of two columns"), width=4),
            ],
            justify="start",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of two columns"), width=6, className='bg-primary p-4', style={'fontFamily': 'Inconsolata'}),
                dbc.Col(html.Div("One of two columns"), width=6, className='bg-danger display-4'),
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of two columns"), width=4),
                dbc.Col(html.Div("One of two columns"), width=4),
            ],
            justify="end",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of two columns"), width=4),
                dbc.Col(html.Div("One of two columns"), width=4),
            ],
            justify="between",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of two columns"), width=4),
                dbc.Col(html.Div("One of two columns"), width=4),
            ],
            justify="around",
        ),
    ]
)


homepage_layout = [header, body, row]

@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return f'You have selected "{value}"'
