#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
from flask import Flask, render_template


# In[10]:


import requests
url = "https://ero.betfair.com/www/sports/exchange/readonly/v1/bymarket?_ak=nzIFcwyWhrlwYMrh&currencyCode=GBP&locale=en_GB&marketIds=1.128151441&rollupLimit=10&rollupModel=STAKE&types=MARKET_STATE,RUNNER_STATE,RUNNER_EXCHANGE_PRICES_BEST,RUNNER_DESCRIPTION"
url2 = "https://ero.betfair.com/www/sports/exchange/readonly/v1/bymarket?_ak=nzIFcwyWhrlwYMrh&alt=json&currencyCode=GBP&locale=en_GB&marketIds=1.170917778,1.128988348&rollupLimit=10&rollupModel=STAKE&types=MARKET_STATE,RUNNER_STATE,RUNNER_EXCHANGE_PRICES_BEST"

payload = {}
headers = {
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/plain, */*',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
  'DNT': '1',
  'Origin': 'https://www.betfair.com',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://www.betfair.com/',
  'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
  'Cookie': '__cfduid=d3013254245c8d86c0aae9e7a0fe0cd661604447496; wsid=8246db31-1e2f-11eb-b7f4-fa163ea4ad04; vid=fa6d8bae-3b04-4a6b-b4f4-76df1b3615de; bfsd=ts=1604447498682|st=p; storageSSC=lsSSC%3D1; xsrftoken=a0a7a690-1e2f-11eb-9f1a-fa163e8a430a; PI=3013; StickyTags=rfr=3013; TrackingTags=; pi=partner3013; rfr=3013; exp=ex; language=en_GB; betexPtk=betexCurrency%3DGBP~betexTimeZone%3DEurope%2FLondon~betexRegion%3Dundefined~betexLocale%3Den_GB; betexPtkSess=betexCurrencySessionCookie%3DGBP~betexLocaleSessionCookie%3Den_GB~betexRegionSessionCookie%3DGBR'

}

response = requests.request("GET", url, headers=headers, data = payload)


# In[11]:


#unpack the data from the json - odds snapshot
df=pd.json_normalize(json.loads(response.text),record_path=["eventTypes","eventNodes","marketNodes","runners"],meta=["eventTypes"], errors="ignore")


# In[12]:


#unpack the timestamp and metadata
df2=df.eventTypes.apply(pd.Series).eventNodes.apply(pd.Series)[0].apply(pd.Series).marketNodes.apply(pd.Series)[0].apply(pd.Series).state.apply(pd.Series)


# In[13]:


#combine metadata with odds data
final_df=pd.concat([df,df2.reindex(df.index)],axis=1)


# In[14]:


final_df


# In[15]:


final_df.to_csv("data.csv",mode='a',header=False)


# In[15]:


app = Flask(__name__)


@app.route("/") 
def home(): 
	df = plot_data()
	return render_template('index.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)


# In[ ]:


import plotly.express as px


# In[14]:


def plot_data():
    df_to_plot=pd.read_csv("data.csv")
    df_to_plot=df_to_plot[(df_to_plot['description.runnerName']=='Joe Biden')|(df_to_plot['description.runnerName']=='Donald Trump')]
    pivot = df_to_plot.pivot_table(index='lastMatchTime', columns='description.runnerName' ,values ='state.lastPriceTraded')
    return pivot


# In[3]:





# In[9]:





# In[12]:




