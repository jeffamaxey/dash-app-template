from flask import Flask
import dash
import dash_auth

from config import dict_logins

server = Flask(__name__)

app = dash.Dash(server=server,
                suppress_callback_exceptions=True,
                assets_folder='/assets')

app.title = 'dkhosla Dash App Template'

auth = dash_auth.BasicAuth(app,
                           dict_logins)
