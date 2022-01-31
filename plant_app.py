import dash
import dash_bootstrap_components as dbc
import dash_auth

## DB Imports
from db.connect_db import *

## DB Connection
conn = connect_to_db(db_name='house_plants')

### USERNAME AND PASS
VALID_USERNAME_PASSWORD_PAIRS = [
    ['ramosem97', 'PlantApp123']
]

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server
app.config.suppress_callback_exceptions = True