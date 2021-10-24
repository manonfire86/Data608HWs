import pandas as pd
import numpy as np
import jupyter_dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from plotly import graph_objs as go
from dash.dependencies import Input, Output


url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json'
trees = pd.read_json(url)

#What proportion of trees are in good, fair, or poor health according to the ‘health’ variable ?


trees['spc_common'] = trees['spc_common'].fillna('Missing')
trees['health'] = trees['health'].fillna('Missing')

q_1_health = pd.DataFrame(trees.groupby(['boroname','spc_common','health'])['tree_id'].count())


q_1_health_prop = q_1_health.div(q_1_health.sum(level=[0,1]))


q_1_health_prop_un = q_1_health_prop.unstack(level=1)



temp_df = q_1_health_prop_un.reset_index().melt(id_vars=['boroname','health'])
temp_df = temp_df.fillna(0)
temp_df = temp_df[temp_df['health']!='Missing']


health = temp_df.health.unique()
query = [str(i) for i in range(0,50000,2000)]
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([        
        html.Div([
            html.Label('Query'),
            dcc.Dropdown(
                id='query_dropdown',
                options=[{'label' : q, 'value' : q} for q in query],
                clearable=False,
                value=query[0]
            ),
        ]),
        html.Div([
            html.Label('Health'),
            dcc.Dropdown(
                id='health_dropdown',
                options=[{'label' : x, 'value' : x} for x in health],
                clearable=False,
                value=health[0]
            ),
        ]),
    ]),
    dcc.Graph(id='bar-chart', figure=go.Figure())
])


@app.callback(
    Output("bar-chart", "figure"), 
    [Input("query_dropdown", "value"),
     Input("health_dropdown", "value")])
def update_bar_chart(query,health):
    url = 'https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit= '.replace(' ',query)
    trees = pd.read_json(url)
    trees['spc_common'] = trees['spc_common'].fillna('Missing')
    trees['health'] = trees['health'].fillna('Missing')
    q_1_health = pd.DataFrame(trees.groupby(['boroname','spc_common','health'])['tree_id'].count())
    q_1_health_prop = q_1_health.div(q_1_health.sum(level=[0,1]))
    q_1_health_prop_un = q_1_health_prop.unstack(level=1)
    temp_df = q_1_health_prop_un.reset_index().melt(id_vars=['boroname','health'])
    temp_df = temp_df.fillna(0)
    temp_df = temp_df[temp_df['health']!='Missing']
    mask = temp_df["health"] == health
    fig = px.bar(temp_df[mask],x='spc_common',y='value',color='boroname',barmode='group') 
    fig.update_layout(title_text='Species Health Ratio Across Burroughs')
    return fig

if __name__ == '__main__':
    app.run_server()
