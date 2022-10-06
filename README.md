# Visualization-dash-python

import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import cdata.mysql as mod
import plotly.graph_objs as go
 
cnxn = mod.connect("User=myUser;Password=myPassword;Database=NorthWind;Server=myServer;Port=3306;")
 
df = pd.read_sql("SELECT ShipName, Freight FROM Orders WHERE ShipCountry = 'USA'", cnxn)
app_name = 'dash-mysqldataplot'
 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'CData + Dash'
trace = go.Bar(x=df.ShipName, y=df.Freight, name='ShipName')
 
app.layout = html.Div(children=[html.H1("CData Extension + Dash", style={'textAlign': 'center'}),
dcc.Graph(
id='example-graph',
figure={
'data': [trace],
'layout':
go.Layout(title='MySQL Orders Data', barmode='stack')
})
], className="container")
 
if __name__ == '__main__':
app.run_server(debug=True)
