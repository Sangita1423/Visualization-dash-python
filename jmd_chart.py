#import all module
from dataclasses import replace
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,ALL,State,MATCH,ALLSMALLER
import plotly.express as px
import pandas as pd
import numpy as np

import pyodbc
import sqlalchemy as sal
from sqlalchemy import create_engine

def get_y_vars(action, variables_j,variables_z):
    
    server = '10.1.1.142'
    database = 'UNOFINANCE_REPORT' 
    username = 'uno' 
    password = 'devmis123'  
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    # select 26 rows from SQL table to insert in dataframe.

    #variables_j = variables_j.replace("[","")
    #variables_j = variables_j.replace("]","")
    # print("Action is :"+action)

    if(action=="JMD"):
        # if len(variables_j)>0:
        #     print(" variables_j  is :")
        #     print(variables_j)
        #     query = "select   Left(JMDGRPUNIT,3) JMDGRPUNIT , sum(amount) 'amount' from  ExpDumpAsonDate_Final  where  Left(JMDGRPUNIT,3) in("+variables_j+") and  isnull(JMDGRPUNIT,'') <> '' and isnull(ZONEGRPUNIT,'') <> ''group by JMDGRPUNIT  ;"            
        # elif len(variables_j) ==0:
        #    query = "select   Left(JMDGRPUNIT,3) JMDGRPUNIT , sum(amount) 'amount' from  ExpDumpAsonDate_Final  where isnull(JMDGRPUNIT,'') <> '' and isnull(ZONEGRPUNIT,'') <> ''group by JMDGRPUNIT  ;"

        query = "select JMDGRPUNIT , sum(amount) 'amount' from  ExpDumpAsonDate_Final  where isnull(JMDGRPUNIT,'') <> '' and isnull(ZONEGRPUNIT,'') <> ''group by JMDGRPUNIT ;"

    if(action=="JMDZONE"):
        # if len(variables_j)>0:
        #     print(" variables_j  is :")
        #     print(variables_j)
        #     query = "select   Left(JMDGRPUNIT,3) JMDGRPUNIT , sum(amount) 'amount' from  ExpDumpAsonDate_Final  where  Left(JMDGRPUNIT,3) in("+variables_j+") and  isnull(JMDGRPUNIT,'') <> '' and isnull(ZONEGRPUNIT,'') <> ''group by JMDGRPUNIT  ;"            
        # elif len(variables_j) ==0:
        #    query = "select   Left(JMDGRPUNIT,3) JMDGRPUNIT , sum(amount) 'amount' from  ExpDumpAsonDate_Final  where isnull(JMDGRPUNIT,'') <> '' and isnull(ZONEGRPUNIT,'') <> ''group by JMDGRPUNIT  ;"

        query = "select ZONEGRPUNIT , sum(amount) 'amount' from  ExpDumpAsonDate_Final  where isnull(ZONEGRPUNIT,'') <> '' and isnull(ZONEGRPUNIT,'') <> ''group by ZONEGRPUNIT ;"
    if(action=="ZONE"):

        #query = "select JMDGRPUNIT,ZONEGRPUNIT , sum(amount) 'amount'  from  ExpDumpAsonDate_Final where  JMDGRPUNIT in("+variables_j+") and isnull(JMDGRPUNIT,'') <> '' and isnull(ZONEGRPUNIT,'') <>'' group by JMDGRPUNIT,ZONEGRPUNIT order by JMDGRPUNIT;"
        query ="Exec sp_testpython_data @P_JMD="+ variables_j + "  ,@P_ZONE="+ variables_z
        # print(" query is" +query)
        # cursor.execute(query)
        # df = []
        # result = cursor.fetchall()
        # while result:
        #     col_names = [x[0] for x in cursor.description]
        #     data = [tuple(x) for x in result]  # convert pyodbc.Row objects to tuples
        #     df.append(pd.DataFrame(data, columns=col_names))
        #     if cursor.nextset():
        #         result = df.fetchall()
        #     else:
        #         result = None
        # print("df is ")
        # print(df)
        # return df
        #query = "select ZONEGRPUNIT , sum(amount) from  ExpDumpAsonDate_Final_test  where ZONEGRPUNIT is not null group by ZONEGRPUNIT;"
    if(action=="UNIT"):
        query = "select JMDGRPUNIT,ZONEGRPUNIT,UnitShrtDescr as UNIT , sum(amount)  amount from  ExpDumpAsonDate_Final where ZONEGRPUNIT is not null and JMDGRPUNIT in('"+variables_j+"')   and ZONEGRPUNIT in('"+variables_z+"') group by JMDGRPUNIT,ZONEGRPUNIT,UnitShrtDescr;"
        #query = "select ZONEGRPUNIT , sum(amount) from  ExpDumpAsonDate_Final_test  where ZONEGRPUNIT is not null group by ZONEGRPUNIT;"
    
    
    df = pd.read_sql(query, cnxn)
    return df

app = dash.Dash(__name__)

df = get_y_vars("JMD","","")
JMD =[]
for ind in df.index:
    #print(df['JMDGRPUNIT'][ind])
    # if df['JMDGRPUNIT'][ind] == df['JMDGRPUNIT'][ind-1]:
    #     print("")
    # else:    
        JMD.append(df['JMDGRPUNIT'][ind])

dfz = get_y_vars("JMDZONE","","")
JMDZONE =[]
for ind in dfz.index:
    #print(df['JMDGRPUNIT'][ind])
    JMDZONE.append(dfz['ZONEGRPUNIT'][ind])

# dfu = get_y_vars("UNIT","GU1","CENTRAL TN ZONE")
# JMDUNIT =[]
# for ind in dfu.index:
#     #print(df['JMDGRPUNIT'][ind])
#     JMDUNIT.append(dfu['UNIT'][ind])

app.layout = html.Div([
    html.Div(children=[
        html.Button('Add chart',id='add-chart',n_clicks=0),
    ]),
    html.Div(id='container',children=[])
])

@app.callback(
    Output('container','children'),
    [Input('add-chart','n_clicks')],
    [State('container','children')]
)
def display_graphs(n_clicks,div_children):
    new_child= html.Div(
        style={'width':'75%','display':'inline-block','outline':'thin lightgrey solid','padding':'1%'},
        children=[
            dcc.Graph(
                id={
                    'type':'dynamic-graph',
                    'index':n_clicks
                },
                figure={}
            ),
            dcc.RadioItems(
                id={
                    'type':'dynamic-choice',
                    'index':n_clicks
                },
                options=[{'label':'Bar chart','value':'bar'},
                         {'label':'Line chart','value':'line'},
                         {'label':'Pie chart','value':'pie'}],
                value='pie',
             ),
             dcc.Dropdown(
                 JMD,id={'type':'dynamic-dpn-s','index':n_clicks},multi=True,value=""
             ),
             dcc.Dropdown(
                 JMDZONE,id={'type':'dynamic-dpn-num','index':n_clicks},multi=True,value=""
             )                        
        ]
    )
    div_children.append(new_child)
    return div_children

@app.callback(
    Output({'type':'dynamic-graph','index':MATCH},'figure'),
    [Input(component_id={'type':'dynamic-dpn-s','index': MATCH},component_property='value'),
     #Input(component_id={'type':'dynamic-dpn-s','index': MATCH},component_property='value'),
     Input(component_id={'type':'dynamic-dpn-num','index': MATCH},component_property='value'),
     Input({'type':'dynamic-choice','index':MATCH},'value')],
     prevent_intial_call=False
)
       
def update_graph(s_value,num_value,chart_choice):
    print("num_value 1")
    print(num_value)
    print("s_value 2")
    print(s_value)
    
    counterz = 0
    counterzstr= "'"
    for item in num_value:
        counterz = counterz +1
        print(counterz)
        if counterz == 1:
            counterzstr =  counterzstr + str(item) +"" 
        else:
            counterzstr = counterzstr +","+ str(item) + ","
        print("counterz value is :")   
        print(counterzstr)
    
    
    counterzstr = counterzstr + "'" 

    counterj = 0
    counterjstr= "'"
    for item in s_value:
        counterj = counterj +1
        print(counterj)
        if counterj == 1:
            counterjstr =  counterjstr + str(item) +"" 
        else:
            counterjstr = counterjstr +","+ str(item) + ","
        print("counterj value is :")   
        print(counterjstr)
    
    
    counterjstr = counterjstr + "'" 
    
    print(counterj)
    print(counterjstr)

    if counterj > 0:
        print("counterzstr is :")
        print(counterzstr)
        dff = get_y_vars("ZONE",counterjstr,"''")
        #dff = dfnew[dfnew["JMDGRPUNIT"].isin(s_value)]
        #filter2 = dfz[dfz["ZONEGRPUNIT"].isin(num_value)]
        #print(dff)
        #print(filter2)
        #dff = df
    else:    
        dff = get_y_vars("JMD","","")
        print(dff)
        #dff = df
        #dff = df[df["JMDGRPUNIT"].isin(['CENTRAL TN ZONE', 'KNCHI AND SALEM ZONE'])]
    if counterz > 0:
        print("counterzstr is :")
        print(counterzstr)
        dff = get_y_vars("ZONE",counterjstr,counterzstr)
        #print(df["ZONEGRPUNIT"])
        #print(num_value)
        #counterzstr = counterzstr[0:len(counterzstr)-1]
        #dff = get_y_vars("ZONE","",counterzstr)
        #dff = dfnew[dfnew["JMDGRPUNIT"].isin(num_value)]
        # print(dff) 
        #dff = df

    #dff = df[df["JMDGRPUNIT"].isin(s_value)]
    #dff = df[filter1 & filter2]
    #dff  = filter1
    

    if chart_choice == 'bar':
        #dff  =dff.groupby([s_value],as_index=False)[['GU1','GU2','GU3','GU4','GU5']]
        #fig = px.bar(dff,x=s_value,y="amount")
        if counterj > 0 and counterz > 0:
            print("condition 1")
            fig =px.bar(dff,values="amount",names="JMDGRPUNIT")
        elif counterj > 0:
            print("condition 2")
            fig =px.bar(dff,values="amount",names="JMDGRPUNIT")
        elif counterz > 0:
            print("condition 3")
            fig =px.bar(dff,values="amount",names="JMDGRPUNIT")
        else:
            print("condition 4")
            fig =px.bar(x=dff["amount"],y=dff["JMDGRPUNIT"])
        return fig
    elif chart_choice == 'line':
        #dff =dff.groupby([ctg_value],as_index=False)[dfu['UNIT']]
        fig = px.line(dff,x='JMDGRPUNIT',y='amount')
        return fig
    elif chart_choice == 'pie':
        fig = px.pie(dff,values=dff["amount"],names=dff["JMDGRPUNIT"])
        return fig
    
#run the app
app.run_server(debug=True)


 

