from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from plant_app import app
# import all pages in the app
from apps import home, new_plant, edit_plant, display_plant

# building the navigation bar
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/home"),
        dbc.DropdownMenuItem("New Plant", href="/new-plant"),
        dbc.DropdownMenuItem("Edit Plant", href="/edit-plant"),
        dbc.DropdownMenuItem("Display Plant", href="/display-plant"),
        
    ],
    nav = True,
    in_navbar = True,
    label = "Options",
)
navbar = dbc.Navbar(
    
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [   
                        dbc.Col(html.Img(src='assets\images\\navbar_image.jpg', height="50px",className='img')),
                        dbc.Col(dbc.NavbarBrand("House Plants", className="ml-2")),
                    ],
                    align="center",
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)
### Toggle Navigation Bar
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

### embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')
               ])
def display_page(pathname):
    
    if pathname == '/new-plant':
        return new_plant.layout
    elif pathname == '/display-plant':
        return display_plant.layout
    elif pathname == '/edit-plant':
        return edit_plant.layout
    else:
        return home.layout

if __name__ == '__main__':
    
    ### Test or Real
    test = 1
    
    if test == 1:
        # import os
        # os.remove("db\\house_plants.db")

        app.run_server(debug=True)
    else:
        app.run_server(debug=False, host='0.0.0.0', port=9000)