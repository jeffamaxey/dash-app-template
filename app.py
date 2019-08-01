from flask import Flask
import dash

server = Flask(__name__)

app = dash.Dash(name='dkhosla dash app template',
                server=server,
                suppress_callback_exceptions=True,
                static_folder='/assets')
