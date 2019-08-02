import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Output, Input

from app import app
# will be used for callbacks

from src import list_14_markets, get_initial_submission_table

# ----------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------

header = dbc.Row(children=[
    dbc.Col(html.Img(src='/assets/logo.png',
                     height='50px'),
            width='auto',
            align="center"),
    dbc.Col('App Title',
            className="display-4 text-uppercase font-weight-bold",
            width=True,
            align="center"),
    ],
                 className='p-3 bg-dark text-white',
                 style={'fontFamily': 'Inconsolata'})

# ----------------------------------------------------------------------
# WIDGET 1
# ----------------------------------------------------------------------
widget_1 = dbc.Row(children=[
    dbc.Col(dcc.Dropdown(id='dropdown-market',
                         options=[{'label': i, 'value':f"{i}"}
                                  for i in list_14_markets],
                         searchable=False,
                         clearable=False,
                         placeholder="Select Market"),
            width=6,
            className="p-3",
            align='center'),
    dbc.Col(dcc.Slider(id='slider-target-lau',
                       min=80_000,
                       max=200_000,
                       step=1_000,
                       value=80_000,
                       marks={k:f"{k:,d}" for k in range(80_000, 200_000, 25_000)}),
            width=6,
            className="p-3",
            align='center'),
    dbc.Col(html.Div(id='show-selected-target',
                     className='border p-4'),
            width=6,
            align='center')],
                   className="p-5 text-center",
                   justify='center',
                   style={'fontFamily': 'Inconsolata',
                          'fontSize': 'x-large'})


@app.callback(
    Output("show-selected-target", 'children'),
    [Input("slider-target-lau", 'value'),
     Input("dropdown-market", 'value')
     ])
def read_slider_for_target_lau(slider_value, dropdown_value):
    """
    """
    if dropdown_value not in list_14_markets:
        return ''
    else:
        result = get_initial_submission_table(MARKET=dropdown_value,
                                              LAU_TARGET=slider_value)
        print(result)

        df = result.get('lau_by_pillar')

        print(df)

        return dbc.Table.from_dataframe(df,
                                        striped=True,
                                        bordered=True,
                                        hover=True)


# assemble components into layout
components_layout = [
    header,
    widget_1
]
