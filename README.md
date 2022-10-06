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





# Connecting to mysql database
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt


mydb = mysql.connector.connect(host="localhost",
							user="root",
							password="password",
							database="student_info")
mycursor = mydb.cursor()

# Fecthing Data From mysql to my python progame
mycursor.execute("select Name, Marks from student_marks")
result = mycursor.fetchall

Names = []
Marks = []

for i in mycursor:
	Names.append(i[0])
	Marks.append(i[1])
	
print("Name of Students = ", Names)
print("Marks of Students = ", Marks)


# Visulizing Data using Matplotlib
plt.bar(Names, Marks)
plt.ylim(0, 5)
plt.xlabel("Name of Students")
plt.ylabel("Marks of Students")
plt.title("Student's Information")
plt.show()


