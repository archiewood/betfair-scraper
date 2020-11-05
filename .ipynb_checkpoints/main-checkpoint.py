#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import get_data
from flask import Flask, render_template, redirect, url_for


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


@app.route("/refresh")
def refresh_data():
    get_data.pull_data_to_db()
    return redirect(url_for('home'))