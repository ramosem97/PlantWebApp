### Imports
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

import os

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

## App Import
from plant_app import app, conn

## Get Data
# conn = connect_to_db(db_name='house_plants')
inventory = pd.read_sql('SELECT * FROM plant_inventory', conn)
plant_info = pd.read_sql('SELECT * FROM plant_details', conn)
## Merge Invetory with Info
plants = inventory.merge(plant_info, on=['PlantInfoID'], how='left').sort_values(['PurchaseDate']).reset_index(drop=True)


####################################################
#################START OF APP#######################
####################################################

input_components = ['common_name', 
                    'scientific_name',
                    'plant_type',
                    'plant_desc', 
                    'size',
                    'purchased_date',
                    'potted_date',
                    'light_req',
                    'water_req',
                    'temp_req',
                    'humid_req',
                    'toxicity',
                    'origin',
                    'comments',
                    'plant_photo']

NOT_EMPTY = ['common_name', 
            'scientific_name',
            'plant_type',
            'purchased_date',
            'size',
            'plant_photo']

# Create App
layout = html.Div([
    
    dbc.Col([
        
        
        
        ####################################################
        #################INPUT COMPONENTS###################
        ####################################################
        
        dbc.Collapse([  
                      
            dbc.Row([
                html.H4('Existing Plant or New Plant?', style={'textAlign':'left'}),
                html.Br(),
                html.Div('If plant is not available below, then select New Plant', style={'textAlign':'left'}),
                html.Br(),
                dcc.Dropdown(
                    options=[{'label': 'New Plant', 'value':'new'}] + \
                        [{'label': x+' - '+y, 'value':x} for x,y in plant_info[['CommonName', 'ScientificName']].values],
                    value=None,
                    multi=False,
                    id='plant_name_dropdown'
                ),
            ], style={'width':'70%', 'margin-left':'15%', 'margin-right':'15%', 'textAlign':'center'}),
            html.Br(),
                     
        ], is_open=True, id='plant_name_dropdown_collapse'),
        
        ####################################################
        ############## Basic Plant Desc ####################
        ####################################################
        #'common_name','scientific_name','size','comments'
         
        dbc.Collapse([   
                      
            dbc.Row([html.H4('General Info')]
                    , style={'width':'50%', 'margin-left':'20%', 'margin-right':'30%', 'textAlign':'left'}),
            html.Br(),
                
            dbc.Row([
            
                dbc.Col([
                
                                    
                    ### Common Name Text Box
                    dbc.Row([
                        html.H5('Plant Name', style={'textAlign':'left'}),
                        html.Br(),
                        
                        dcc.Input(id='common_name', placeholder='Ex: String of Turtles', type='text', style={}, value=None),
                    ], style={}),
                    html.Br(),
                    
                    ### Scientific Name Text Box
                    dbc.Row([
                        html.H5('Scientific Name', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.Input(id='scientific_name', placeholder='Ex: Peperomia prostata', type='text', style={}, value=None),
                    ], style={}),
                    html.Br(),
                
                    ### Plant Type
                    dbc.Row([
                        html.H5('Plant Type', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.Input(id='plant_type', placeholder='Ex: Peperomia', type='text', style={}, value=None),
                    ], style={}),
                    html.Br(),
                    
                    ### Plant Desc
                    dbc.Row([
                        html.H5('Plant Description', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.Input(id='plant_desc', placeholder='Ex.: Peperomia', type='text', style={}, value=None),
                    ], style={}),
                    html.Br(),
                    
                    ### Size of Plant 
                    dbc.Row([
                        html.H5('Plant Size', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.Slider(
                            min=2,
                            max=12,
                            marks={i: '{}in'.format(i) for i in range(2, 13, 2)},
                            step=2,
                            value=None,
                            id='plant_size'
                        )
                    ], style={}),
                    html.Br(),
                
                    ### Dates Purchased and Potted
                    dbc.Row([
                        dbc.Col([
                            html.H5('Date Aquired', style={'textAlign':'left'}),
                            # html.Br(),
                            dcc.DatePickerSingle(
                                id='purchased_date',
                                min_date_allowed=date(2020, 10, 21),
                                max_date_allowed=date.today(),
                                initial_visible_month=date.today(),
                                date=date.today(),
                                display_format='DD/MM/YYYY',
                            ),
                        ], style={'textAlign':'left'}),
                        
                        dbc.Col([
                            html.H5('Date Potted', style={'textAlign':'left'}),
                            # html.Br(),
                            dcc.DatePickerSingle(
                                id='potted_date',
                                min_date_allowed=date(2020, 10, 21),
                                max_date_allowed=date.today(),
                                initial_visible_month=date.today(),
                                placeholder='Not Potted',
                                display_format='DD/MM/YYYY',
                            ),
                        ], style={'textAlign':'left'}),
                        
                    ], style={}),
                    html.Br(),
                
                ], style={}),
                
            ], style={'width':'40%', 'margin-left':'30%', 'margin-right':'30%', 'textAlign':'center'}),
            
        ], is_open=False, id='gen_info'),
        
        ####################################################
        ############## Plant Requirements ##################
        ####################################################
        #'light_req','water_req','toxicity','comments'
        
        dbc.Collapse([
            dbc.Row([html.H4('About the Plant')]
                , style={'width':'50%', 'margin-left':'20%', 'margin-right':'30%', 'textAlign':'left'}),
            html.Br(),
            
            dbc.Row([
                
                dbc.Col([
                    
                    ### Light Requirements Text Box
                    dbc.Row([
                        html.H5('Light Requirements', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Full Sun', 'value': 'Full Sunlight'},
                                {'label': 'Partial Sun', 'value': 'Partial Sunlight'},
                                {'label': 'Indirect Light', 'value': 'Indirect Light'},
                                {'label': 'Full Shade', 'value': 'Full Shade'},
                                ],
                                value=None,
                                id='light_req'
                            ),
                    ], style={}),
                    html.Br(),
                    
                    ### Water Requirements Text Box
                    dbc.Row([
                        html.H5('Water Requirements', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Very Dry', 'value': 'Very Dry'},
                                {'label': 'Moderately Dry', 'value': 'Moderately Dry'},
                                {'label': 'Moderately Wet', 'value': 'Moderately Wet'},
                                {'label': 'Always Wet', 'value': 'Always Wet'},
                                ],
                                value=None,
                                id='water_req'
                            ),
                    ], style={}),
                    html.Br(),
                    
                    ### Toxicity Requirements Dropdown Box
                    dbc.Row([
                        
                        html.H5('Plant Toxicity', style={'textAlign':'left'}),                    
                        html.Br(),
                        dcc.Dropdown(
                            options=[
                                {'label': 'Safe', 'value': 'Safe'},
                                {'label': 'Toxic to Pets', 'value': 'Toxic to Pets'},
                                {'label': 'Toxic to Humans', 'value': 'Toxic to Humans'},
                                {'label': 'Toxic to Everything', 'value': 'Toxic to Everything'},
                                ],
                                value=None,
                                id='toxicity'
                            ),
                        
                    ], style={}),
                    html.Br(),
                    
                    
                ]),
                
                # dbc.Col([], style={'width':'5%'}),
                
                #### Second Part of Requirements
                dbc.Col([
                    
                    ### Humidity Requirements Text Box
                    dbc.Row([
                        html.H5('Humidity Requirements', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.RangeSlider(
                            id='humid_req',
                            min=30,
                            max=100,
                            step=5,
                            value=[60, 80],
                            marks={i: '{}%'.format(i) for i in range(20, 101, 20)},
                        ),
                    ], style={}),
                    html.Br(),
                    
                    ### Temperature Requirements Range Slider
                    dbc.Row([
                        html.H5('Temperature Requirements', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.RangeSlider(
                            id='temp_req',
                            min=30,
                            max=100,
                            step=5,
                            value=[60, 80],
                            marks={i: '{}F'.format(i) for i in range(20, 101, 20)}
                        ),
                    ], style={}),
                    html.Br(),
                    
                    ### Origin Text Box
                    dbc.Row([
                        
                        html.H5('Plant Origin', style={'textAlign':'left'}),
                        html.Br(),
                        dcc.Input(id='origin', placeholder='Ex: South America', type='text', style={}, value=None),
                        
                    ], style={}),
                    html.Br(),
                    
                ], style={}),

                        
            ], style={'width':'50%', 'margin-left':'25%', 'margin-right':'25%', 'textAlign':'center', 'margin-bottom':'30px'}),
        ], id='reqs'),
            
        ####################################################
        ############## Upload Plant Photo ##################
        ####################################################
        
        dbc.Collapse([
            dbc.Row([html.H4('Photos of Plant')]
                    , style={'width':'50%', 'margin-left':'20%', 'margin-right':'30%', 'textAlign':'left'}),
            html.Br(),
            
            dbc.Row([
                
                ### Upload Photo Option
                dcc.Upload( id='plant_photo',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Photo'),
                        ' of Plant' 
                    ]),
                    style={
                        'align': 'center',
                        'width': '100%',
                        'lineHeight': '50px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '3px',
                        'textAlign': 'center',
                        'margin': '5px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=True
                ),
                html.Div(id='output-image-upload')
            
            ], style={'width':'60%', 'textAlign':'center', 'margin-right':'20%', 'margin-left':'20%', 'margin-bottom':'30px'}),
           
        ], is_open=False, id='photo_of_plant'),
        ####################################################
        ############## Submit Button #######################
        ####################################################
        
        dbc.Collapse([
            
            dbc.Row(children=[
                
                dbc.Row([
                    html.Button(id='submit-button', type='submit', children='Add New Plant', 
                                style={'width':'40%','textAlign':'center', 'margin-left':'30%', 'margin-right':'30%'})
                ]),
                dbc.Row([
                    html.Div(children=[], id='output-submit-button', 
                                style={})
                ]),

            ], style={'width':'90%', 'textAlign':'center', 'margin-left':'5%', 'margin-right':'5%', 'margin-top':'5%'})
            
        ], is_open=False, id='submit_button_collapse'),
        
    ])
    
], style={'width':'95%', 'height':'100%', 'margin-bottom':'5%', 'display': 'flex', 'flex-direction': 'row'})

    
################################################################
################# Add Plant Callback Functions #################
################################################################

################ DropDown-Plant Information #################

@app.callback(
                [
                    Output("gen_info", "is_open"),
                    Output("reqs", "is_open"),
                    Output("photo_of_plant", "is_open"),
                    Output("submit_button_collapse", "is_open"),
                    Output("plant_name_dropdown_collapse", 'is_open'),
                    Output('common_name', 'disabled'),
                    Output('scientific_name', 'disabled'),
                    Output('plant_type', 'disabled'),
                    Output('plant_desc', 'disabled'),
                    Output('light_req', 'disabled'),
                    Output('water_req', 'disabled'),
                    Output('temp_req', 'disabled'),
                    Output('humid_req', 'disabled'),
                    Output('toxicity', 'disabled'),
                    Output('origin', 'disabled'),
                    Output('common_name', 'value'),
                    Output('scientific_name', 'value'),
                    Output('plant_type', 'value'),
                    Output('plant_desc', 'value'),
                    Output('light_req', 'value'),
                    Output('water_req', 'value'),
                    Output('temp_req', 'value'),
                    Output('humid_req', 'value'),
                    Output('toxicity', 'value'),
                    Output('origin', 'value'),
                    
                ],
                [
                    Input('plant_name_dropdown', 'value')
                ],
                []
            )

def get_plant_details(name):
    print('Name: ', name)
    output_valL = ['common_name', 'scientific_name', 'plant_type', 'plant_desc',
                        'light_req','water_req','temp_req', 'humid_req','toxicity','origin']
    
    output_collapseL = [False, False, False, False, True]
    output_new_valL = [None, None, None, None, None, None, [60, 80], [60, 80], None, None]
    output_disabledL = [False, False, False, False, False, False, False, False, False, False]
    
    if name!=None:
        
        output_collapseL = [True, True, True, True, True]
        
        if name =='new':
            print('Hello')
            output_new_valL = ['', '', '', '', '', None, [60, 80], [60, 80], None, '']
            output_disabledL = [False, False, False, False, False, False, False, False, False, False]
            
        else:
            
            output_disabledL = [True, True, True, True, True, True, True, True, True, True]
            plant_entry = plant_info.loc[plant_info['CommonName']==name]
            
            if len(plant_entry) != 1:
                print('ERROR: More Than One Entry')
            # print(len(plant_entry), plant_entry.columns)
            
            output_new_valL = [plant_entry['CommonName'].values[0], plant_entry['ScientificName'].values[0], plant_entry['PlantType'].values[0], \
                                plant_entry['PlantDesc'].values[0], plant_entry['LightRequirements'].values[0], plant_entry['WaterRequirements'].values[0], \
                                [plant_entry['TemperatureRequirementsMin'].values[0], plant_entry['TemperatureRequirementsMax'].values[0]], \
                                [plant_entry['HumidityRequirementsMin'].values[0], plant_entry['HumidityRequirementsMax'].values[0]], \
                                plant_entry['Toxicity'].values[0], plant_entry['Origin'].values[0]]
                
    
    return output_collapseL[0], output_collapseL[1], output_collapseL[2], output_collapseL[3], output_collapseL[4], \
            output_disabledL[0], output_disabledL[1], output_disabledL[2], output_disabledL[3], output_disabledL[4], \
            output_disabledL[5], output_disabledL[6], output_disabledL[7], output_disabledL[8], output_disabledL[9], \
            output_new_valL[0], output_new_valL[1], output_new_valL[2], output_new_valL[3], output_new_valL[4], \
            output_new_valL[5], output_new_valL[6], output_new_valL[7], output_new_valL[8], output_new_valL[9]


################# Add Plant Function #################

# def save_image(name, content):
#     data = content.encode("utf8").split(b";base64,")[1]
    
#     # with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
#     #     fp.write(base64.decodebytes(data))
    
def plant_db_entry(common_name, scientific_name, plant_type, plant_desc, 
                   plant_size, purchased_date, potted_date,
                   light_req, water_req, temp_req, humid_req, 
                   toxicity, origin, new_plant):
    
    
    ###### Add Plant Details
    if new_plant == 'new':
        
        plant_info_id = plant_info['PlantInfoID'].max() + 1
        
        plant_dets_new = pd.DataFrame([], columns=plant_info.columns)
        plant_dets_new = plant_dets_new.append({
                                'PlantInfoID':plant_info_id,
                                'CommonName':common_name, 'ScientificName':scientific_name,
                                'PlantType':plant_type, 'PlantDesc':plant_desc,
                                'LightRequirements':light_req, 'WaterRequirements':water_req, 
                                'TemperatureRequirementsMin':temp_req[0], 'TemperatureRequirementsMax':temp_req[1], 
                                'HumidityRequirementsMin':humid_req, 'HumidityRequirementsMax':humid_req, 
                                'Toxicity':toxicity, 'Origin':origin, 'Other':'',
                            }, ignore_index = True)
        
        plant_dets_new.set_index(['PlantInfoID']).to_sql('plant_details', conn, if_exists='append')
        
        
    else:
        plant_dets = plant_info.loc[plant_info['CommonName']==new_plant]
        plant_info_id = plant_dets['PlantInfoID'].values[0]
        
    ###### Add Plant Inventory
        print(inventory['PlantID'].values)
        print([int(x[1:]) for x in inventory['PlantID'].values])
        plant_id = 'P' + str(np.max([int(x[1:]) for x in inventory['PlantID'].values]) + 1).zfill(4)
                
        plant_inv_new = pd.DataFrame([], columns=inventory.columns)
        plant_inv_new = plant_inv_new.append({
                                'PlantID':plant_id,
                                'Active':1, 'Iteration':1,
                                'PlantInfoID':plant_info_id,
                                'Size':plant_size, 'PurchaseDate':purchased_date,
                                'PottedDate':potted_date, 'Comments':'',
                            }, ignore_index = True)
        
        # print(plant_inv_new)
        plant_inv_new.set_index(['PlantID']).to_sql('plant_inventory', conn, if_exists='append')
    
    return plant_id

def save_image_in_folder(plant_id, plant_size, img_contents, img_date):
    
    ## Get Plant Folder Path
    plant_folder = os.getcwd() + '\\assets\\images\\{pid}\\{size}'\
        .format(pid=plant_id, size=plant_size)
    
    ## Create Folder if it does not exist
    if not os.path.exists(plant_folder):
        os.makedirs(plant_folder)
        
    ## Save Photos
    count = 1
    for content, date in zip(img_contents, img_date):
        
        ## Convert TimeStamp to Date
        date = datetime.fromtimestamp(date)
        
        ## Get File Name
        fname = "{pid}_{year}_{month}_{day}_{count}.jpg".format(pid=plant_id, 
                                                            year=str(date.year),
                                                            month=str(date.month).zfill(2),
                                                            day=str(date.day).zfill(2),
                                                            count=count)
        
        ## Save File
        import base64
        
        data = content.encode("utf8").split(b";base64,")[1]
        with open(os.path.join(plant_folder, fname), "wb") as fp:
            fp.write(base64.decodebytes(data))
        
        count += 1
    

# input_components = ['common_name', 
#                     'scientific_name',
#                     'plant_type',
#                     'plant_desc', 
#                     'size',
#                     'purchased_date',
#                     'potted_date',
#                     'light_req',
#                     'water_req',
#                     'temp_req',
#                     'humid_req',
#                     'toxicity',
#                     'origin',
#                     'comments',
#                     'plant_photo']

# NOT_EMPTY = ['common_name', 
#             'scientific_name',
#             'plant_type',
#             'purchased_date',
#             'size',
#             'plant_photo']
                 
@app.callback(Output("output-submit-button", "children"),
              [
                    Input('submit-button', 'n_clicks')],
              [
                    State('common_name', 'value'),
                    State('scientific_name', 'value'),
                    State('plant_type', 'value'),
                    State('plant_desc', 'value'),
                    State('purchased_date', 'date'),
                    State('potted_date', 'date'),
                    State('plant_size', 'value'),
                    State('light_req', 'value'),
                    State('water_req', 'value'),
                    State('temp_req', 'value'),
                    State('humid_req', 'value'),
                    State('toxicity', 'value'),
                    State('origin', 'value'),
                    State('plant_name_dropdown', 'value'),
                    State('plant_photo', 'contents'),
                    State('plant_photo', 'last_modified')
              ],
            )
def submit_new_plant(clicks, 
                     common_name, scientific_name, plant_type, plant_desc,
                     purchased_date, potted_date, plant_size,
                     light_req, water_req, temp_req, humid_req, toxicity,origin,new_plant,
                     img_contents, img_date):
    print('CALLBACK: Submit New Plant')
    # print('INPUT: ', clicks, common_name, scientific_name, plant_size, light_req, water_req, toxicity)
    
    input_dict = {
                    'Plant Name': common_name, 
                    'Scientific Name': scientific_name, 
                    'Plant Type': plant_type, 
                    'Plant Desc': plant_desc, 
                    'Plant Size': plant_size, 
                    'Light Requirements': light_req, 
                    'Water Requirements': water_req, 
                    'Toxicity': toxicity, 
                    'Image Contents': img_contents,
                    'Image Date': img_date,
                 }
    
    if clicks is not None:
    
        ## Check if Inputs are All Uploaded
        emptyL = []
        for key, val in input_dict.items():
            
            if (val == '') or (val == None):
                emptyL.append(key)
        
        # If There are Empty inputs 
        if len(emptyL) > 0:
            msg = 'ERROR: Missing Input for {empty}.'.format(empty=', '.join(emptyL))
            return html.Div(msg, style={'color':'red'})

        #### If All Info is Correctly Inputed
        else:
            msg = 'Successfully Added New Plant!'
            
            
            ### Get Plant Info for DB Entry and Enter Plant data into DB
            plant_id = plant_db_entry(common_name, scientific_name, plant_type, plant_desc, 
                                                                  plant_size, purchased_date, potted_date,
                                                                    light_req, water_req, temp_req, humid_req, 
                                                                    toxicity, origin, new_plant)
            
            
                        
            ### Create PID Folder and Save Image in It
            save_image_in_folder(plant_id, plant_size, img_contents, img_date)
                        
            ### Go to Home Page
            return  dcc.Location(pathname="/home", id="")
    
    else:
        msg = ''
        return  html.Div(msg)


################# Upload Plant Image Function #################
    
def parse_contents(contents, filename, date):
    return dbc.Col([
        html.H5(filename, style={}),
        html.H6(datetime.fromtimestamp(date)),
        html.Img(src=contents, style={'width':'30%'}),
        html.Hr(),
    ])

@app.callback(Output('output-image-upload', 'children'),
              Input('plant_photo', 'contents'),
              State('plant_photo', 'filename'),
              State('plant_photo', 'last_modified'))
def update_image_output(image_contents, image_filenames, image_dates):

    if image_contents is not None:
        # print(len(image_contents))
        children = dbc.Row(
                    [parse_contents(c, n, d) for c, n, d in zip(image_contents, image_filenames, image_dates)]
                    , style={'width':'100%'})
        return children