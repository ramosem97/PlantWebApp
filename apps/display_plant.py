### Imports
import pandas as pd
import numpy as np

import glob
import os
import datetime

import dash
from dash import dash_table as dt
from dash import html as html
import plotly.graph_objects as go
from dash import dcc as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State

## DB Imports
from db.connect_db import *

### Global Vars
num_display_max = 10

## Get Data
conn = connect_to_db(db_name='house_plants')
inventory = pd.read_sql('SELECT * FROM plant_inventory', conn)
plant_info = pd.read_sql('SELECT * FROM plant_details', conn)
## Merge Invetory with Info
plants = inventory.merge(plant_info, on=['PlantInfoID'], how='left').sort_values(['PurchaseDate']).reset_index(drop=True)

####################################################
################# HELPER FUNCTIONS #################
####################################################

#### Function to Create Dash Component for Displaying One Plant
def display_plant(plant_entry):

    plant_folder = os.getcwd() + '\\assets\\images\\{pid}'.format(pid=plant_entry['PlantID'])
    plants_imgs = np.sort(glob.glob('{folder}\\*.jpg'.format(folder=plant_folder))) 
    plant_curr_imgs = [img.split('\\')[-1] for img in plants_imgs]
    
    if len(plants_imgs) == 0:
        return html.Div()
    
    else:
        plant_disp = dbc.Row([
            dbc.Col([
                dbc.Row([ 
                        html.H6('{cname} - {sname}'\
                        .format(cname=plant_entry['CommonName'], sname=plant_entry['ScientificName']), 
                            style={}),
                ]),
                    
                    # html.H6(datetime.datetime.fromtimestamp(date), style={}),
                dbc.Row(
                    
                    html.Img(src='\\assets\\images\\{pid}\\{fname}'.format(pid=plant_entry['PlantID'], fname=plant_curr_imgs[-1]))
                    
                , style={'width':'30%', 'textAlign':'center', 'margin-right':'35%', 'margin-left':'35%'}),
            ]),
            
        ], style={'width':'40%', 'textAlign':'center', 'margin-right':'30%', 'margin-left':'30%', 'margin-bottom':'2%'})
        
    
    return plant_disp



####################################################
################ START OF APP ######################
####################################################

curr_plant = None
# Create App
layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', 
            children = 'Current Plant: {}'.format(curr_plant), 
            style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
        
    
    dbc.Col([
        
        dbc.Row([
            
            ######### Plant Picture and Desc  
            dbc.Col(
                
                ########## Plant Picture and Desc
                [display_plant(row) for idx, row in plants.head(1).iterrows()]
                
            , style={'width':'50%'}    ),
            
        ]),
        
    ])
        
])