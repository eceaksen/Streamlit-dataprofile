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
#for animation
import time
import requests
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import json
#for autentication
import streamlit_authenticator as stauth
import pickle
from pathlib import Path


#---Change the data to csv file---
def convert_df(df):
    return df.to_csv().encode('utf-8')
#
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
#Page Tabs
st.set_page_config(page_title="Yeni Nesil Teknolojiler")

#authentication
names=["john","timmy"]
usernames=["smith", "turner"]
passwords=["11","22"]

#file_path=Path(__file__).parent /"hashed_pw.pkl"
#with file_path.open("rb") as file:
#    hashed_passwords=pickle.load(file)
hashed_passwords = stauth.Hasher(passwords).generate()

authenticator=stauth.authenticate(names,usernames,hashed_passwords,"Yeni Nesil Teknolojiler","abcdef",cookie_expiry_days=30)
name,authentication_status1, username=authenticator.login("Login","main")

if authentication_status1==False:
    st.error("Usernam/pass is incoorrect")
if authentication_status1==None:
    st.warning("enter username password")
if authentication_status1:
    #Menu Type1
    authenticator.logout("Logout", "Sidebar")
    st.sidebar.title(f"Hoşgeldiniz {name}")
    with st.sidebar:
        page = option_menu("Menü", ["Ana Sayfa", "Talep Analizi", "SLA Süre Analizi", 'Sweetviz Raporu'],
            icons=['house', 'cloud-upload', "list-task", 'gear'], menu_icon="cast", default_index=0)
        page

    #Menu Type2
    #page = option_menu(None, ["Home Page", "Detailed Request Analysis", "Sla Duration Analysis", 'Sweetviz Report'],
    #    icons=['house', 'cloud-upload', "list-task", 'gear'],
    #    menu_icon="cast", default_index=0, orientation="horizontal")
    #    page



    #Dataset
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

    if page=="Ana Sayfa":
        # Animation
        lottie_hello = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_ye2v3dmd.json")
        st_lottie(lottie_hello, speed=1, reverse=False, loop=True, quality="low", height=None, width=None, key=None)

        #----------
        st.caption("Yükleniyor")
        bar = st.progress(50)
        for percent_complete in range(100):
            time.sleep(0.00001)
            bar.progress(percent_complete + 1)
        st.balloons()
        st.success('Tamamlandı')

        #st.image("/Users/eceaks/PycharmProjects/streamlite/img0.jpg")
        st.markdown("<h1 style='text-align:center;'>YENİ NESİL TEKNOLOJİLER</h1>",unsafe_allow_html=True)
        st.title("""İstek Performans Raporu""")
        st.caption("Analizler BTYP Raporları kullanılarak oluşturulmuştur.")
        # ---------------
        st.subheader("İstek Raporu (Btyp & Tableu Entegre) ")
        st.caption("Projeye Bağlanmamış Uygulama Destek Taleplerinin Detay Raporudur.")
        st.write(df1)

        # ---------------
        st.header("Talep Durum Dağılımı")
        st.caption("""Pasta Grafiği Analizi""")
        tab1,tab2=st.tabs(["Versiyon 1","Versiyon 2"])
        with tab1:
            st.write("Versiyon 1 Tipi Grafik")
            pie_chart = px.pie(df2, values='#ofRequest', names="RequestType")
            st.plotly_chart(pie_chart)
        with tab2:
            st.write("Versiyon 2 Tipi Grafik")
            valuec = df1["Durumu"].value_counts()
            fig, ax = plt.subplots()
            ax.pie(valuec, autopct='%0.2f%%', labels=['Açık', 'Kapalı'])
            st.pyplot(fig)

        with st.expander("Detayları Görmek için Tıklayınız"):
            st.dataframe(valuec)

        #********
        st.header("Talep Tipi Dağılımı")
        rec=df1["RequesType"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(rec, autopct='%0.2f%%', labels=['Hata', 'Yeni İstek', 'İyileştirme/Değişiklik'])
        st.pyplot(fig)

        with st.expander("Detayları Görmek için Tıklayınız"):
            st.dataframe(rec)

        #********

        # ---------------
        st.subheader("Raporu İndir")
        csv = convert_df(df1)
        st.write(emoji.emojize('İstek Raporu (Btyp & Tableu Entegre) :receipt:'))
        st.download_button(
            label="CSV dosyası indir",
            data=csv,
            file_name='btyp_data.csv',
            mime='text/csv',
        )
        # ---------------


    elif page == "Talep Analizi":
        lottie_hello = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_je2kc06t.json")
        st_lottie(lottie_hello, speed=1, reverse=False, loop=True, quality="low", height=None, width=None, key=None)

        with st.spinner("Yükleniyor"):
            time.sleep(2)
        #---------
        st.title("Detaylı Talep Analizi")

        st.subheader('Talep Sınıfları')
        for i in classtype:
            st.markdown("""
                    #### <span style="color:blue">{temp1}</span> <span style="font-size:12pt">{temp}</span>  """.format(
                temp1="*", temp=i), unsafe_allow_html=True)

        with st.expander("Görmek için Tıkla -> Her Sınıf Tipi İçin Talep Sayısı"):
            st.write(df1["ClassType"].value_counts())
        #-----------------
        st.subheader('Talep Modülleri')
        for i in classmodule:
            st.markdown("""
                    #### <span style="color:green">{temp1}</span> <span style="font-size:12pt">{temp}</span>  """.format(
                temp1="*", temp=i), unsafe_allow_html=True)
        with st.expander("Görmek için Tıkla -> Her Modül Tipi İçin Talep Sayısı"):
            st.write(df1["ModuleType"].value_counts())

        #-----------------------------------
        tabv1,tabv2=st.tabs(["Sınıf Tipi","Modül Tipi"])
        with tabv1:
            #---------
            st.subheader("Her Sınıf Tipinden Gelen Talep Sayısı")
            a=df1['ClassType'].value_counts().reset_index()
            a=pd.DataFrame(a)
            a.columns =['ClassType', 'NumberofRequest']
            pie_chart2 = px.pie(a, title='Talep Dağılımı', values=a['NumberofRequest'], names='ClassType')
            st.plotly_chart(pie_chart2)
        with tabv2:
            st.header("Her Modül Tipinden Gelen İstek Sayısı")
            b = df1['ModuleType'].value_counts().reset_index()
            b = pd.DataFrame(b)
            b.columns = ['ModuleType', 'NumberofRequest']
            pie_chart3 = px.pie(b, title='Her Modül için Talep Dağılımı', values=b['NumberofRequest'], names='ModuleType')
            st.plotly_chart(pie_chart3)

        #-------------------------------------------------------------
        st.subheader("Tüm Talepler")
        tab1, tab2 = st.tabs(["Sınıf Tipi","Modül Tipi"])
        with tab1:
            st.write("Sınıf Tipi / Talep Sayısı")
            classtype_nmbr = pd.DataFrame(df1['ClassType'].value_counts())
            st.bar_chart(classtype_nmbr)
        with tab2:
            st.write("Modül Tipi / Talep Sayısı")
            classmodule_nmbr = pd.DataFrame(df1['ModuleType'].value_counts())
            st.bar_chart(classmodule_nmbr)
        st.subheader("Kapalı / Açık Talepler")
        tab1, tab2 = st.tabs(["Sınıf Tipi","Modül Tipi"])
        with tab1:
            st.write("Modül Tipi / Talep Sayısı")
            closereqdf = df1[df1.Durumu == 'Kapalı']
            classmodule_nmbr_cr = pd.DataFrame(closereqdf['ModuleType'].value_counts())
            st.bar_chart(classmodule_nmbr_cr)
        with tab2:
            st.write("Modül Tipi / Talep Sayısı")
            openreqdf = df1[df1.Durumu == 'Açık']
            classmodule_nmbr_or = pd.DataFrame(openreqdf['ModuleType'].value_counts())
            st.bar_chart(classmodule_nmbr_or)

            # Detailed Pie CHart Anaylsis
            st.subheader("Detay Analizler")
            path = st.multiselect("Değişken Seçimi:", (
                'Durumu', 'İstek Sahibi', 'Istek_Sorumlusu', 'Request_Manager', 'Şirket', 'Istek_Tipi', 'RequesType',
                'ClassType', 'ModuleType'))
            fig = px.sunburst(data_frame=df1, path=path)
            st.plotly_chart(fig)

    elif page == "SLA Süre Analizi":
        #---------------------------------------
        lottie_hello = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_eIXuIz.json")
        st_lottie(lottie_hello, speed=1, reverse=False, loop=True, quality="low", height=None, width=None, key=None)

        #Waiting time
        with st.spinner("wait"):
            time.sleep(1)
        #-----------------------------------------
        st.title("SLA Süre Analizi")
        st.subheader("Her Sınıf Tipi için SLA Süre Analizi ")
        tab1, tab2 = st.tabs(["Versiyon 1", "Versiyon 2"])
        # Box Plot Version 1
        with tab1:
            chart2 = ('RPA', 'ZES EV IOT', 'MOBİL UYGULAMALAR', 'INTRANET SİTELERİ', 'Optimizasyon Portali')
            chart_selection2 = st.selectbox("Sınıf Tipi Seçin1", chart2)
            dataf2rpa = df1[df1["ClassType"] == chart_selection2]

            fig=px.box(data_frame=dataf2rpa, x="ClassType", y="Sla_Duration", color="ClassType")
            st.plotly_chart(fig)
            #----------------
        # Box Plot Version 2
        with tab2:
            chart = ('RPA', 'ZES EV IOT', 'MOBİL UYGULAMALAR', 'INTRANET SİTELERİ', 'Optimizasyon Portali')
            chart_selection = st.selectbox("Sınıf Tipi Seçin2", chart)
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

        st.subheader("Talep vs SLA Süresi")
        unique_Sla_Duration = df1['Sla_Duration'].unique().tolist()
        moduleselect=st.slider('Sla Süresi', min_value=min(unique_Sla_Duration),max_value=max(unique_Sla_Duration),value=(min(unique_Sla_Duration),max(unique_Sla_Duration)))

        typeofmodul=st.multiselect('Birden Fazla Sınıf Tipi Seçebilirsiniz',classtype, default=classtype)
        tryout=(df1["Sla_Duration"].between(*moduleselect))& (df1['ClassType'].isin(typeofmodul))
        number_of_result=df1[tryout].shape[0]
        st.markdown(f'*Belirlenmiş Sla Süresi Aralığında Bulunan Mevcut Talep sayısı : {number_of_result}*' )

        #-----------------------------------------------------------------------
        # Scatter Plot
        st.subheader("Sla Süresi / Talep Numarası")
        st.write("Opsiyonlar: Sınıf Tipi, Modül Tipi, Talep Tipi")
        tab1, tab2 = st.tabs(["Versiyon 1", "Versiyon 2"])
        # Version 1 Scatter Plot
        with tab1:
            selectopt = st.selectbox('Kategori Seçimi', ("ClassType", "ModuleType", "RequesType"))
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
        #Summary Table
        st.subheader('Talep Tarihi/Sla Süresi/Sınıf Tipi')
        fig = go.Figure(data=go.Table(
            header=dict(values=list(df1[['Request_Date', "Istek_Numarası", 'Sla_Duration', 'ClassType']].columns),
                        fill_color='#FD8E72', align='center'),
            cells=dict(values=[df1.Request_Date, df1.Istek_Numarası, df1.Sla_Duration, df1.ClassType], fill_color='#E5ECF6',
                       align='left')))
        # fig.update_layout()
        st.write(fig)

        # ---------------
        # KONTROL ET!!
        st.write("Grafikler Kontrol Edilecek!!")
        st.header("Talep Yoğunluğu")
        st.write(emoji.emojize(':chart_increasing:'))
        line = pd.DataFrame(df1['Request_Date'].value_counts())
        st.line_chart(line)
        # ---------------
        st.subheader("Total Activity Duration - (Request Types-ClassType)")
        piv = df1.pivot_table(index="RequesType", columns="ClassType", values="ToplamAktiviteSüresi")
        st.write(piv)
        st.subheader("Total Sla Duration - (Request Types-ClassType)")
        piv2 = df1.pivot_table(index="RequesType", columns="ClassType", values="Sla_Duration")
        st.write(piv2)


    elif page=="Sweetviz Raporu":
        st.title("Sweetviz Raporu")
        st.write("Otomatik Rapor Çıktısı")

        st.caption("Yükleniyor")
        bar = st.progress(50)
        for percent_complete in range(100):
            time.sleep(0.00001)
            bar.progress(percent_complete + 1)
        st.success('Tamamlandı')


        st.write(emoji.emojize('Check it from the next tab :thumbs_up:'))
        my_report = sv.analyze(df1)
        my_report.show_html()


        lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ncztkceu.json")
        st_lottie(lottie_hello, speed=1, reverse=False, loop=True, quality="low", height=None, width=None, key=None)

    #st.graphviz_chart(''' digraph{
    #              step1 -> A ->
    #              step2-> B
    #              step3-> C
    #              step4-> D }''')

    # Emoji list: https://unicode.org/emoji/charts/full-emoji-list.html
    # Not for the recommended libraries(Link: https://towardsdatascience.com/5-less-known-python-libraries-that-can-help-in-your-next-data-science-project-5970a81b32de?gi=b580e2c8d052):
    #1- PyForest:use this library for personal use only. If you work with a team and use PyForest, others won’t know which libraries you’ve imported.
    #2- Faker: Generates fake data
    #3- Mito: Only jupiter notebook or jupiter lab
    #4- Opendatasets: Reach to any open dataset easily.