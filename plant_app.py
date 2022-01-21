### Imports
import pandas as pd
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub

from sklearn.metrics.pairwise import linear_kernel

import dash
from dash import dash_table as dt
from dash import html as html
import plotly.graph_objects as go
from dash import dcc as dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output, State



app = dash.Dash()

df = px.data.stocks()
stockL = [x for x in df.columns.tolist() if x != 'date']

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', 
            children = 'Styling using html components', 
            style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
        options = [
            {'label':'All', 'value':'all' },
            {'label':'Google', 'value':'GOOG' },
            {'label': 'Apple', 'value':'AAPL'},
            {'label': 'Amazon', 'value':'AMZN'},
            {'label': 'Facebook', 'value':'FB'},
            {'label': 'Netflix', 'value':'NFLX'},
            {'label': 'Microsoft', 'value':'MSFT'},
            ],
        value = 'all'),
        dcc.Graph(id = 'line_plot'),
        
        dt.DataTable(
            id='table', data=df.round(2).tail(10).to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
        ),
        
    ])
    
    
@app.callback(Output(component_id='line_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])

def graph_update(dropdown_value):
    print(dropdown_value)
    
    if dropdown_value != 'all':
        fig = go.Figure([go.Scatter(x = df['date'], y = df['{}'.format(dropdown_value)],\
                        line = dict(color = 'firebrick', width = 4))
                        ])
    else:
        fig = go.Figure()
        # for stock in stockL:
        #     fig.add_trace(go.Scatter(x=df['date'], y=df[stock],
        #                 mode='lines',
        #                 name=stock))
            
        df['mean'] = df[stockL].mean(axis=1)
        df['1pos_std'] = df['mean'] + df[stockL].std(axis=1)
        df['1neg_std'] = df['mean'] - df[stockL].std(axis=1)
        
        fig.add_trace(go.Scatter(x=df['date'], 
                                 y=df['mean'],
                                 fill=None,
                                 mode='lines',
                                 name='Mean',
                                 line=dict(width=3,
                                           color='black')))
        
        fig.add_trace(go.Scatter(x=df['date'], 
                                 y=df['1pos_std'],
                                 fill=None,
                                 mode='lines',
                                 name='Upper Bound',
                                 line=dict(width=.2,
                                           color='lightsteelblue')))
        fig.add_trace(go.Scatter(
                                x=df['date'],
                                y=df['1neg_std'],
                                fill='tonexty', # fill area between trace0 and trace1
                                mode='lines', 
                                name='Lower Bound',
                                 line=dict(width=.2,
                                           color='lightsteelblue')))
    
    fig.update_layout(title = 'Stock prices over time',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices'
                      )
    return fig  
    
    

if __name__ == '__main__': 
    app.run_server(debug=True)