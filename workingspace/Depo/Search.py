import streamlit as st
import pandas as pd
import plotly.express as px
#from PIL import Image
import altair as alt
from vega_datasets import data
import plotly.graph_objects as go
import sweetviz as sv
import emoji
import time
import numpy as np
import graphviz as graphviz


#Page Tabs
st.set_page_config(page_title="General Information")

tabs=["Ana Sayfa","Açık Talepler","Tamamlanan Talepler"]
page=st.sidebar.radio("Sekmeler",tabs)

dataset=st.container()
interactive=st.container()

with dataset:
    datasource = '/Users/eceaks/PycharmProjects/streamlite/dataset2.xlsx'
    sheet_n1 = 'data1'
    df1 = pd.read_excel(datasource, sheet_name=sheet_n1, usecols='A:V', header=0)

if page=="Main Page":
    st.write("bla")

elif page == "Açık Talepler":
    #Atalep1= df1.groupby("ClassType").count()
    Atalep2=df1[df1["Durumu"]=="Açık"]
    #st.write(Atalep1)
    st.write(Atalep2)

elif page == "Tamamlanan Talepler":
    st.write("bla")
