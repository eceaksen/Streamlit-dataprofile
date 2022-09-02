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
import seaborn as sns
from bokeh.plotting import figure #more difficult much more useful
from streamlit_option_menu import option_menu

#---Change the data to csv file---
def convert_df(df):
    return df.to_csv().encode('utf-8')

#Page Tabs
st.set_page_config(page_title="General Information")

#Menu Type1
with st.sidebar:
    page = option_menu("Menu", ["Home Page", "Detailed Request Analysis", "Sla Duration Analysis", 'Sweetviz Report'],
        icons=['house', 'cloud-upload', "list-task", 'gear'], menu_icon="cast", default_index=1)
    page

#Menu Type2
#page = option_menu(None, ["Home Page", "Detailed Request Analysis", "Sla Duration Analysis", 'Sweetviz Report'],
#    icons=['house', 'cloud-upload', "list-task", 'gear'],
#    menu_icon="cast", default_index=0, orientation="horizontal")



dataset=st.container()
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

if page=="Home Page":

    st.subheader("Progress bar")
    bar = st.progress(50)
    for percent_complete in range(100):
        time.sleep(0.00001)
        bar.progress(percent_complete + 1)
    st.balloons()
    st.success('Done')


    st.image("/Users/eceaks/PycharmProjects/streamlite/img0.jpg")
    st.markdown("<h1 style='text-align:center;'>New Generation Technologies</h1>",unsafe_allow_html=True)
    st.title("""Support Request Report""")
    st.caption("Analyzes were created from data obtained from BTYP.")
    # ---------------
    st.header("**BTYP** Dataset")
    st.write("Detailed Report of Support Tickets")
    st.write(df1)

    st.header("Open/Closed Request Distribution")
    st.subheader("""Pie Chart Analysis""")
    tab1,tab2=st.tabs(["Version 1","Version 2"])
    with tab1:
        st.subheader("Version 1 Chart")
        pie_chart = px.pie(df2, title='Request Overview', values='#ofRequest', names="RequestType")
        st.plotly_chart(pie_chart)

    with tab2:
        st.subheader("Version 2 Chart")
        valuec = df1["Durumu"].value_counts()
        # st.write(valuec)
        fig, ax = plt.subplots()
        ax.pie(valuec, autopct='%0.2f%%', labels=['Açık', 'Kapalı'])
        st.pyplot(fig)
        #st.dataframe(valuec)

    with st.expander("Click to See Chart Details"):
        st.dataframe(valuec)

    #********
    st.header("Request Type Distribution")

    rec=df1["RequesType"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(rec, autopct='%0.2f%%', labels=['Hata', 'Yeni İstek', 'İyileştirme/Değişiklik'])
    st.pyplot(fig)

    with st.expander("Click to See-> Request Type Details"):
        st.dataframe(rec)

    #********

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


elif page == "Detailed Request Analysis":
    st.image("/Users/eceaks/PycharmProjects/streamlite/img2.jpg")
    with st.spinner("wait"):
        time.sleep(3)
    #---------
    st.title("Detailed Request Analysis")
    st.header('List of Class Types')
    for i in classtype:
        st.markdown("""
                #### <span style="color:blue">{temp1}</span> <span style="font-size:12pt">{temp}</span>  """.format(
            temp1="*", temp=i), unsafe_allow_html=True)

    with st.expander("Click to See -> Number of Requests For Each Class Type"):
        st.write(df1["ClassType"].value_counts())

    st.header('List of Module Types')
    for i in classmodule:
        st.markdown("""
                #### <span style="color:green">{temp1}</span> <span style="font-size:12pt">{temp}</span>  """.format(
            temp1="*", temp=i), unsafe_allow_html=True)
    with st.expander("Click to See -> Number of Requests For Each Module Type"):
        st.write(df1["ModuleType"].value_counts())

    tabv1,tabv2=st.tabs(["Class Type","Module Type"])

    with tabv1:
        #---------
        st.header("Number of Request From Each Class Type")
        a=df1['ClassType'].value_counts().reset_index()
        a=pd.DataFrame(a)
        a.columns =['ClassType', 'NumberofRequest']
        pie_chart2 = px.pie(a, title='Request Overview', values=a['NumberofRequest'], names='ClassType')
        st.plotly_chart(pie_chart2)
    #----------

    with tabv2:
        st.header("Number of Request From Each Module Type")
        b = df1['ModuleType'].value_counts().reset_index()
        b = pd.DataFrame(b)
        b.columns = ['ModuleType', 'NumberofRequest']
        pie_chart3 = px.pie(b, title='Request Overview', values=b['NumberofRequest'], names='ModuleType')
        st.plotly_chart(pie_chart3)
        # ----------------
    #Detailed Pie CHart Anaylsis
    st.header("Detailed Cathegorical Variable Analysis")
    path = st.multiselect("Select feature", (
    'Durumu', 'İstek Sahibi', 'Istek_Sorumlusu', 'Request_Manager', 'Şirket', 'Istek_Tipi', 'RequesType',
    'ClassType', 'ModuleType'))
    fig = px.sunburst(data_frame=df1, path=path)
    st.plotly_chart(fig)


    st.header("All Requests")
    tab1, tab2 = st.tabs(["Class Type", "Module Type"])
    with tab1:
        st.subheader("Class Type / #of Request")
        classtype_nmbr = pd.DataFrame(df1['ClassType'].value_counts())
        st.bar_chart(classtype_nmbr)
    with tab2:
        st.subheader("Module Type / #of Request")
        classmodule_nmbr = pd.DataFrame(df1['ModuleType'].value_counts())
        st.bar_chart(classmodule_nmbr)
    st.header("Close / Open Requests")
    tab1, tab2 = st.tabs(["Close Requests", "Open Requests"])
    with tab1:
        st.subheader("Module Type / #of Request")
        closereqdf = df1[df1.Durumu == 'Kapalı']
        classmodule_nmbr_cr = pd.DataFrame(closereqdf['ModuleType'].value_counts())
        st.bar_chart(classmodule_nmbr_cr)
    with tab2:
        st.subheader("Module Type / #of Request")
        openreqdf = df1[df1.Durumu == 'Açık']
        classmodule_nmbr_or = pd.DataFrame(openreqdf['ModuleType'].value_counts())
        st.bar_chart(classmodule_nmbr_or)


elif page == "Sla Duration Analysis":
    #---------------------------------------
    #Waiting time
    with st.spinner("wait"):
        time.sleep(3)

    st.title("Sla Duration Analysis")
    st.header("SLA Duration Analysis For Each Class Type ")
    # ---------------------------------------
    tab1, tab2 = st.tabs(["Versiyon 1", "Versiyon 2"])
    # Box Plot Version 1
    with tab1:
        chart2 = ('RPA', 'ZES EV IOT', 'MOBİL UYGULAMALAR', 'INTRANET SİTELERİ', 'Optimizasyon Portali')
        chart_selection2 = st.selectbox("Select Class Type2", chart2)
        dataf2rpa = df1[df1["ClassType"] == chart_selection2]

        fig=px.box(data_frame=dataf2rpa, x="ClassType", y="Sla_Duration", color="ClassType")
        st.plotly_chart(fig)
        #----------------
    # Box Plot Version 2
    with tab2:
        chart = ('RPA', 'ZES EV IOT', 'MOBİL UYGULAMALAR', 'INTRANET SİTELERİ', 'Optimizasyon Portali')
        chart_selection = st.selectbox("Select Class Type", chart)
        fig, ax = plt.subplots()

        if chart_selection == 'RPA':
            datafrpa = df1[df1["ClassType"] == 'RPA']
            sns.boxplot(x="ClassType", y="Sla_Duration", data=datafrpa, ax=ax)
        elif chart_selection == 'ZES EV IOT':
            datafzes = df1[df1["ClassType"] == 'ZES EV IOT']
            sns.boxplot(x="ClassType", y="Sla_Duration", data=datafzes, ax=ax)
        elif chart_selection == 'MOBİL UYGULAMALAR':
            datafmobil = df1[df1["ClassType"] == 'MOBİL UYGULAMALAR']
            sns.boxplot(x="ClassType", y="Sla_Duration", data=datafmobil, ax=ax)
        elif chart_selection == 'INTRANET SİTELERİ':
            datafintra = df1[df1["ClassType"] == 'INTRANET SİTELERİ']
            sns.boxplot(x="ClassType", y="Sla_Duration", data=datafintra, ax=ax)
        elif chart_selection == 'Optimizasyon Portali':
            datafoptim = df1[df1["ClassType"] == 'Optimizasyon Portali']
            sns.boxplot(x="ClassType", y="Sla_Duration", data=datafoptim, ax=ax)
        st.pyplot(fig)
    #--------------------------------------------------------------------------

    st.header("Request vs Sla Duration")
    unique_Sla_Duration = df1['Sla_Duration'].unique().tolist()
    moduleselect=st.slider('Sla_Duration', min_value=min(unique_Sla_Duration),max_value=max(unique_Sla_Duration),value=(min(unique_Sla_Duration),max(unique_Sla_Duration)))

    typeofmodul=st.multiselect('ClassTypeReq',classtype, default=classtype)
    tryout=(df1["Sla_Duration"].between(*moduleselect))& (df1['ClassType'].isin(typeofmodul))
    number_of_result=df1[tryout].shape[0]
    st.markdown(f'*Number of Request exist between the given Sla_Duration period: {number_of_result}*' )

    #-----------------------------------------------------------------------
    # Scatter Plot
    st.header("Sla Duration / Request No -> Class Type, Module Type, Request Type")
    tab1, tab2 = st.tabs(["Versiyon 1", "Versiyon 2"])
    # Version 1 Scatter Plot
    with tab1:
        selectopt = st.selectbox('Select category', ("ClassType", "ModuleType", "RequesType"))
        fig = px.scatter(data_frame=df1, x='Istek_Numarası', y="Sla_Duration", color=selectopt)
        st.plotly_chart(fig)
    #Versiyon 2 Scatter Plot
    with tab2:
        fig, ax = plt.subplots()
        cat_cols = df1.select_dtypes(include=['object']).columns.tolist()
        cat_cols = ['Durumu', 'İstek Sahibi', 'Istek_Sorumlusu', 'Request_Manager', 'Şirket', 'Istek_Tipi', 'RequesType',
                    'ClassType', 'ModuleType']
        hue_type = st.selectbox("check", cat_cols)
        sns.scatterplot(x='Istek_Numarası', y='Sla_Duration', hue=hue_type, ax=ax, data=df1)
        st.pyplot(fig)
    # -----------------------------------------------------------------------
    #Line Graph

    st.header("#of Requests Received on Certain Days")
    st.write(emoji.emojize(':chart_increasing:'))
    line = pd.DataFrame(df1['Request_Date'].value_counts())
    st.line_chart(line)
    # ---------------
    #Summary Table
    # ----------------
    st.header('Request Date/Sla Duration/Class Type')
    fig = go.Figure(data=go.Table(
        header=dict(values=list(df1[['Request_Date', "Istek_Numarası", 'Sla_Duration', 'ClassType']].columns),
                    fill_color='#FD8E72', align='center'),
        cells=dict(values=[df1.Request_Date, df1.Istek_Numarası, df1.Sla_Duration, df1.ClassType], fill_color='#E5ECF6',
                   align='left')))
    # fig.update_layout()
    st.write(fig)
    #---------------
    st.subheader("Total Activity Duration - (Request Types-ClassType)")
    piv = df1.pivot_table(index="RequesType", columns="ClassType", values="ToplamAktiviteSüresi")
    st.write(piv)
    st.subheader("Total Sla Duration - (Request Types-ClassType)")
    piv2 = df1.pivot_table(index="RequesType", columns="ClassType", values="Sla_Duration")
    st.write(piv2)


elif page=="Sweetviz Report":
    st.title("Sweetviz Report")
    st.header("Detailed Analysis of Data")

    st.subheader("Progress bar")
    bar = st.progress(50)
    for percent_complete in range(100):
        time.sleep(0.00001)
        bar.progress(percent_complete + 1)
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