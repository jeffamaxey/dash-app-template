import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app

from pages.components import header
from src import list_14_markets, get_initial_submission_table

dropdown_1 = dcc.Dropdown(id='input-market',
                          options=[
                              {'label': i, 'value':f"{i}"}
                              for i in list_14_markets
                              ],
                          searchable=False,
                          clearable=False,
                          placeholder="Select Market")

slider_1 = dcc.Slider(id='input-lau',
                      min=80_000,
                      max=200_000,
                      step=1_000,
                      value=80_000,
                      marks={k:f"{k:,d}"
                             for k in range(80_000, 200_000, 25_000)})

div_1 = html.Div(id='output-market-lau-1')
div_2 = dcc.Slider(id='output-market-lau-2', min=80_000, max=200_000)


mv_layout = [
    header,
    dbc.Row(dbc.Col(dropdown_1, align='center', className='py-4', width=6), justify='center'),
    dbc.Row(dbc.Col(slider_1, align='center', className='py-4', width=6), justify='center'),
    dbc.Row(dbc.Col(div_1, align='center', className='py-4', width=6), justify='center'),
    dbc.Row(dbc.Col(div_2, align='center', className='py-4', width=6), justify='center'),
]

@app.callback([Output('output-market-lau-1', 'children'),
               Output('output-market-lau-2', 'value')],
              [Input('input-market', 'value'),
               Input('input-lau', 'value')])
def display_selected_values(dropdown_value, slider_value):
    '''Lorem ipsum'''
    if dropdown_value in list_14_markets:
        result = (f"Market={dropdown_value}, and LAU={int(slider_value/10**3):,d}k", slider_value)
    else:
        result = ("Please select a Market and LAU", slider_value)

    return result


result = get_initial_submission_table(MARKET='Germany',
                                      LAU_TARGET=82_000)
df = result.get('lau_by_pillar').reset_index()
df
