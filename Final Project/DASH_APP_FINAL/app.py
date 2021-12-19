import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from plotly import graph_objs as go
from dash.dependencies import Input, Output
import urllib.request

url = "https://api.nomics.com/v1/exchange-markets/ticker?key=m_023109940eb177bbb78f68f84f1d509115b7a741&interval=1d&currency=BTC,ETH,XRP&exchange=binance,gdax,gemini&per-page=100&page=1"

## Market Data Call

market_data = urllib.request.urlopen(url).read()

market_df = pd.io.json.read_json(market_data )

market_subset = market_df[['exchange','type','base','price','last_updated']].copy(deep=True)

## Latest Price Call

query_string = 'ids=' + ','.join(market_subset.base.unique()[0:13])
url2 = 'https://api.nomics.com/v1/currencies/ticker?key=m_023109940eb177bbb78f68f84f1d509115b7a741&{query_string}&interval=1d,30d&convert=USD&per-page=100&page=1'.format(query_string=query_string)

price_data = urllib.request.urlopen(url2).read()

pricing_df = pd.io.json.read_json(price_data)
pricing_subset = pricing_df[['id','price','price_date']]

pricing_vol = pricing_df['1d'].apply(pd.Series)
pricing_vol['volume'] = pd.to_numeric(pricing_vol['volume'])
pricing_vol = pd.concat([pricing_df,pricing_vol],axis=1)


coin = market_subset.base.unique()[0:13]
asset_type = market_subset.type.unique()
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([        
        html.Div([
            html.Label('Currency'),
            dcc.Dropdown(
                id='coin_dropdown',
                options=[{'label' : q, 'value' : q} for q in coin],
                clearable=False,
                value=coin[0]
            ),
        ]),
        html.Div([
            html.Label('Asset Type'),
            dcc.Dropdown(
                id='asset_type_dropdown',
                options=[{'label' : x, 'value' : x} for x in asset_type],
                clearable=False,
                value=asset_type[0]
            ),
        ]),
    ]),
    dcc.Graph(id='scatter-plot', figure=go.Figure()),
html.Div([
    html.Div([        
        html.Div([
            html.Label('Currency'),
            dcc.Dropdown(
                id='coin_dropdown2',
                options=[{'label' : q, 'value' : q} for q in coin],
                clearable=False,
                value=coin[0]
            ),
        ]),
        html.Div([
            html.Label('Asset Type'),
            dcc.Dropdown(
                id='asset_type_dropdown2',
                options=[{'label' : x, 'value' : x} for x in asset_type],
                clearable=False,
                value=asset_type[0]
            ),
        ]),
    ]),
    dcc.Graph(id='scatter-plot2', figure=go.Figure())
    ]),
])

@app.callback(
    Output("scatter-plot", "figure"),
    [Input("coin_dropdown", "value"),
     Input("asset_type_dropdown", "value")])
def update_scatter_plot(coin,asset_type):
    
    url = "https://api.nomics.com/v1/exchange-markets/ticker?key=m_023109940eb177bbb78f68f84f1d509115b7a741&interval=1d&currency=BTC,ETH,XRP&exchange=binance,gdax,gemini&per-page=100&page=1"

    ## Market Data Call

    market_data = urllib.request.urlopen(url).read()

    market_df = pd.io.json.read_json(market_data )

    market_subset = market_df[['exchange','type','base','price','last_updated']].copy(deep=True)
    
    ## Latest Price Call

    query_string = 'ids=' + ','.join(market_subset.base.unique()[0:13])
    url2 = 'https://api.nomics.com/v1/currencies/ticker?key=m_023109940eb177bbb78f68f84f1d509115b7a741&{query_string}&interval=1d,30d&convert=USD&per-page=100&page=1'.format(query_string=query_string)

    price_data = urllib.request.urlopen(url2).read()

    pricing_df = pd.io.json.read_json(price_data)
    pricing_subset = pricing_df[['id','price','price_date']]

    pricing_vol = pricing_df['1d'].apply(pd.Series)
    pricing_vol['volume'] = pd.to_numeric(pricing_vol['volume'])
    pricing_vol = pd.concat([pricing_df,pricing_vol],axis=1)


    # Volume Dataframe
    oneday_volume_df = market_df['1d'].apply(pd.Series)

    # unified dataframe
    unified_df = pd.concat([market_subset,oneday_volume_df],axis=1)
    unified_df['trades'] = pd.to_numeric(unified_df['trades'])
    unified_df['volume'] = pd.to_numeric(unified_df['volume'])

    fig = px.scatter(market_subset[(market_subset['base']==coin)&(market_subset['type']==asset_type)],x='exchange',y='price',color='base') 
    fig.update_layout(title_text='Price (USD) Analysis')
    fig.add_hline(y=np.mean(pricing_subset[pricing_subset['id']==coin]['price']),annotation_text="Market_Price",line_dash="dot")
    fig.add_hline(y=np.mean(market_subset[(market_subset['base']==coin)&(market_subset['type']==asset_type)])[0],annotation_text="Average_Trade_Price",line_dash="dot")
    
    return fig

@app.callback(
    Output("scatter-plot2", "figure"),
    [Input("coin_dropdown2", "value"),
     Input("asset_type_dropdown2", "value")])
def update_scatter_plot(coin,asset_type):
    
    url = "https://api.nomics.com/v1/exchange-markets/ticker?key=m_023109940eb177bbb78f68f84f1d509115b7a741&interval=1d&currency=BTC,ETH,XRP&exchange=binance,gdax,gemini&per-page=100&page=1"

    ## Market Data Call

    market_data = urllib.request.urlopen(url).read()

    market_df = pd.io.json.read_json(market_data )

    market_subset = market_df[['exchange','type','base','price','last_updated']].copy(deep=True)

    ## Latest Price Call

    query_string = 'ids=' + ','.join(market_subset.base.unique()[0:13])
    url2 = 'https://api.nomics.com/v1/currencies/ticker?key=m_023109940eb177bbb78f68f84f1d509115b7a741&{query_string}&interval=1d,30d&convert=USD&per-page=100&page=1'.format(query_string=query_string)

    price_data = urllib.request.urlopen(url2).read()

    pricing_df = pd.io.json.read_json(price_data)
    pricing_subset = pricing_df[['id','price','price_date']]

    pricing_vol = pricing_df['1d'].apply(pd.Series)
    pricing_vol['volume'] = pd.to_numeric(pricing_vol['volume'])
    pricing_vol = pd.concat([pricing_df,pricing_vol],axis=1)

    # Volume Dataframe
    oneday_volume_df = market_df['1d'].apply(pd.Series)

    # unified dataframe
    unified_df = pd.concat([market_subset,oneday_volume_df],axis=1)
    unified_df['trades'] = pd.to_numeric(unified_df['trades'])
    unified_df['volume'] = pd.to_numeric(unified_df['volume'])

    fig =  px.scatter(unified_df[(unified_df['base']==coin)&(unified_df['type']==asset_type)],x='exchange',y='volume',color='base')
    fig.update_layout(title_text='Volume Analysis')    
    fig.add_hline(y=np.mean(pricing_vol[pricing_vol['id']==coin]['volume']),annotation_text="Market_Vol",line_dash="dot")
    fig.add_hline(y=np.mean(unified_df[(unified_df['base']==coin)&(unified_df['type']==asset_type)]['volume']),annotation_text="Average_Exchange_Vol",line_dash="dot")
    
    return fig


if __name__ == '__main__':
    app.run_server()

