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
import matplotlib.pyplot as plt




#---change the data to csv file---
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

#Page Tabs
st.set_page_config(page_title="General Information")

tabs=["Main Page","Pie Chart Analysis","Sla Duration/Request","Bar Chart Analysis", "Line Graph Analysis","Sweetviz Report"]
page=st.sidebar.radio("Sekmeler",tabs)

dataset=st.container()
interactive=st.container()

with dataset:
    datasource = '/Users/eceaks/PycharmProjects/streamlite/dataset2.xlsx'
    sheet_n1 = 'data1'
    df1 = pd.read_excel(datasource, sheet_name=sheet_n1, usecols='A:U', header=0)

    datasource = '/Users/eceaks/PycharmProjects/streamlite/dataset2.xlsx'
    sheet_n2 = 'data2'
    df2 = pd.read_excel(datasource, sheet_name=sheet_n2, usecols='A:B', header=0)

    # ---------------
    classtype = df1['ClassType'].unique().tolist()
    classmodule = df1['ModuleType'].unique().tolist()

closereqdf = df1[df1["Durumu"] == 'Kapalı']
openreqdf = df1[df1.Durumu == 'Açık']
ore=openreqdf["Durumu"].value_counts()
cre=closereqdf["Durumu"].value_counts()
dfyeni=pd.DataFrame()
dfyeni=pd.concat([ore,cre],axis=0)
dfyeni=pd.DataFrame(dfyeni,columns=["Durumu"])


if page=="Main Page":


    #with st.spinner("wait"):
    #    time.sleep(5)
    #st.success('Done')

    st.image("/Users/eceaks/PycharmProjects/streamlite/img0.jpg")
    st.markdown("<h1 style='text-align:center;'>New Generation Technologies</h1>",unsafe_allow_html=True)
    st.title("""Support Request Report""")
    st.write("Analyzes were created from data obtained from BTYP.")
    # ---------------
    st.header("**BTYP** Dataset")
    st.write("Detailed Report of Support Tickets")
    st.write(df1)

    st.header("Open/Close Requests")
    st.write(dfyeni)

    #********

    st.write(df1["RequesType"].value_counts())

    #********

    st.header('List of Class Types')
    for i in classtype:
        st.markdown("""
            #### <span style="color:blue">{temp1}</span> <span style="font-size:12pt">{temp}</span>  """.format(temp1="*",temp=i),unsafe_allow_html=True)
    st.write(df1["ClassType"].value_counts())

    st.header('List of Module Types')
    for i in classmodule:
        st.markdown("""
            #### <span style="color:green">{temp1}</span> <span style="font-size:12pt">{temp}</span>  """.format(temp1="*",temp=i),unsafe_allow_html=True)

    st.write(df1["ModuleType"].value_counts())
    st.subheader("Total Aktivity Duration of Request Types-ClassType")
    piv=df1.pivot_table(index="RequesType" ,columns="ClassType" , values="ToplamAktiviteSüresi")
    st.write(piv)
    st.subheader("Total Sla Duration of Request Types-ClassType")
    piv2 = df1.pivot_table(index="RequesType", columns="ClassType", values="Sla_Duration" )
    st.write(piv2)



    # ---------------
    st.subheader("Export Data")
    csv = convert_df(df1)
    st.write(emoji.emojize('Download Btyp Data :receipt:'))
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='btyp_data.csv',
        mime='text/csv',
    )
    # ---------------





elif page == "Pie Chart Analysis":
    st.title("""Pie Chart Analysis""")

    #---------
    st.header("Number of Request (Open/Closed)")
    pie_chart=px.pie(df2,title='Request Overview',values='#ofRequest',names="RequestType")
    st.plotly_chart(pie_chart)

    st.write("Alternative Chart")
    valuec = df1["Durumu"].value_counts()
    #st.write(valuec)
    fig, ax = plt.subplots()
    ax.pie(valuec, autopct='%0.2f%%', labels=['Açık', 'Kapalı'])
    st.pyplot(fig)
    st.dataframe(valuec)
    #---------
    st.header("Number of Request From Each Class Type")
    a=df1['ClassType'].value_counts().reset_index()
    a=pd.DataFrame(a)
    a.columns =['ClassType', 'NumberofRequest']
    pie_chart2 = px.pie(a, title='Request Overview', values=a['NumberofRequest'], names='ClassType')
    st.plotly_chart(pie_chart2)
    #----------
    st.header("Number of Request From Each Module Type")
    b = df1['ModuleType'].value_counts().reset_index()
    b = pd.DataFrame(b)
    b.columns = ['ModuleType', 'NumberofRequest']
    pie_chart3 = px.pie(b, title='Request Overview', values=b['NumberofRequest'], names='ModuleType')
    st.plotly_chart(pie_chart3)
    # ----------------



elif page == "Sla Duration/Request":
    st.header("Request vs Sla Duration")
    unique_Sla_Duration = df1['Sla_Duration'].unique().tolist()
    moduleselect=st.slider('Sla_Duration', min_value=min(unique_Sla_Duration),max_value=max(unique_Sla_Duration),value=(min(unique_Sla_Duration),max(unique_Sla_Duration)))

    typeofmodul=st.multiselect('ClassTypeReq',classtype, default=classtype)
    tryout=(df1["Sla_Duration"].between(*moduleselect))& (df1['ClassType'].isin(typeofmodul))
    number_of_result=df1[tryout].shape[0]
    st.markdown(f'*Number of Request exist between the given Sla_Duration period: {number_of_result}*' )



elif page== "Bar Chart Analysis":
    #tryout------------
    #--------tryout
    st.header("Class Type vs #of Request -All Requests")
    classtype_nmbr=pd.DataFrame(df1['ClassType'].value_counts())
    st.bar_chart(classtype_nmbr)

    st.header("Module Type vs #of Request - All Requests")
    classmodule_nmbr = pd.DataFrame(df1['ModuleType'].value_counts())
    st.bar_chart(classmodule_nmbr)

    st.header("Module Type vs #of Request - Close Requests")
    closereqdf = df1[df1.Durumu == 'Kapalı']
    classmodule_nmbr_cr= pd.DataFrame(closereqdf['ModuleType'].value_counts())
    st.bar_chart(classmodule_nmbr_cr)

    st.header("Module Type vs #of Request - Open Requests")
    openreqdf = df1[df1.Durumu == 'Açık']
    classmodule_nmbr_or = pd.DataFrame(openreqdf['ModuleType'].value_counts())
    st.bar_chart(classmodule_nmbr_or)


if page=="Line Graph Analysis":

    # ---------------
    st.header("#of Requests Received on Certain Days")
    st.write(emoji.emojize(':chart_increasing:'))
    line = pd.DataFrame(df1['Request_Date'].value_counts())
    st.line_chart(line)
    # ---------------
    st.header('Request Date/Sla Duration/Class Type')
    fig=go.Figure(data=go.Table(header=dict(values=list(df1[['Request_Date',"Istek_Numarası",'Sla_Duration','ClassType']].columns),fill_color='#FD8E72',align='center'), cells=dict(values=[df1.Request_Date,df1.Istek_Numarası,df1.Sla_Duration,df1.ClassType], fill_color='#E5ECF6',align='left')))
    #fig.update_layout()
    st.write(fig)

if page=="Sweetviz Report":

    st.header("Detailed Analysis of Data")

    with st.spinner("wait"):
        time.sleep(5)

    st.subheader("Progress bar")
    bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        bar.progress(percent_complete + 1)
    st.balloons()
    st.success('Done')
    st.graphviz_chart(''' digraph{
          step1 -> A ->
          step2-> B
          step3-> C
          step4-> D }''')
    st.write(emoji.emojize('Check it from the next tab :thumbs_up:'))
    my_report = sv.analyze(df1)
    my_report.show_html()





    # Emoji list: https://unicode.org/emoji/charts/full-emoji-list.html
# Not for the recommended libraries(Link: https://towardsdatascience.com/5-less-known-python-libraries-that-can-help-in-your-next-data-science-project-5970a81b32de?gi=b580e2c8d052):
#1- PyForest:use this library for personal use only. If you work with a team and use PyForest, others won’t know which libraries you’ve imported.
#2- Faker: Generates fake data
#3- Mito: Only jupiter notebook or jupiter lab
#4- Opendatasets: Reach to any open dataset easily.