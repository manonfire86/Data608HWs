# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 20:33:43 2021

@author: HSantana
"""

import pandas as pd
import numpy as np
import urllib.request
import seaborn as sns
import matplotlib.pyplot as plt

url = "https://api.nomics.com/v1/exchange-markets/ticker?key=m_023109940eb177bbb78f68f84f1d509115b7a741&interval=1d&currency=BTC,ETH,XRP&exchange=binance,gdax,gemini&per-page=100&page=1"



## 1d and 30d are nest dictionaries that can be converted into their own dataframe; can be used for volatility analysis
## use candles to build 1 day examination of price ranges 


## Market Data Call

market_data = urllib.request.urlopen(url).read()

market_df = pd.io.json.read_json(market_data )

market_df.columns

market_df.head()

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
## price mapping viz; loop for 5 calls for dfs

## viz prototype

np.mean(pricing_subset[pricing_subset['id']=='BTC']['price'])
np.mean(market_subset[(market_subset['base']=='BTC')&(market_subset['type']=='spot')])[0]
def price_viz_constructor(coin,asset_type):
    sns.scatterplot(x='exchange',y='price',data=market_subset[(market_subset['base']==coin)&(market_subset['type']==asset_type)],hue='base').set(title='Price (USD) Analysis')    
    plt.axhline(pricing_subset()[pricing_subset['id']==coin][['price']].values,color='r',label='Market_Price')
    plt.axhline(np.mean(market_subset[(market_subset['base']==coin)&(market_subset['type']==asset_type)]).values,color='b',label='Average_Trade_Price')
    plt.legend()
    plt.show()


def arb_calc(coin,asset_type):
    return pricing_subset[pricing_subset['id']==coin][['price']].values-np.mean(market_subset[(market_subset['base']==coin)&(market_subset['type']==asset_type)]).values


def vol_viz_constructor(coin,asset_type):
    
    sns.scatterplot(x='exchange',y='volume',data=unified_df[(unified_df['base']==coin)&(unified_df['type']==asset_type)],hue='base').set(title='Volume Analysis')
    
    plt.axhline(pricing_vol[pricing_vol['id']==coin][['volume']].values,color='r',label='Market_Vol')
    plt.axhline(np.mean(unified_df[(unified_df['base']==coin)&(unified_df['type']==asset_type)][['volume']]).values,color='b',label='Average_Exchange_Vol')
    plt.legend()
    plt.show()










