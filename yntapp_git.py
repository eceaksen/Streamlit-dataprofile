import streamlit as st
import pandas as pd
#---
from streamlit_option_menu import option_menu
#---
#Libraries Used For Data Visualization
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
#---
#Libraries Used For Animation
import time
import requests
from streamlit_lottie import st_lottie
import json
#---
#Libraries Used For Autentication
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
#---
import sweetviz as sv #Automatic Report
import emoji #Emoji detecter
#---
#Additional Libraries(Can be used later)
import numpy as np
import graphviz as graphviz
from bokeh.plotting import figure #more difficult much more useful

#############################################################
######                 Functions:                     #######
#############################################################
def convert_df(df): #to convert dataset to csv file
    return df.to_csv().encode('utf-8')
#
def load_lottieurl(url: str): #To get Url of the animation from webpage and transform it to a json file.
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottiefile(filepath: str): #To read json file
    with open(filepath, "r") as f:
        return json.load(f)

#############################################################
######              Configuration of Page             #######

st.set_page_config(page_title="Yeni Nesil Teknolojiler")

#############################################################
######       Configuration of Autentication Page      #######

names = ["Ece", "Adnan","Sevtap","Elif","Yağmur",]
usernames = ["eaksen", "açomakoğlu","ssevgili", "eceyhan","yerışık"]

# Load Hashed Passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,"YNT", "abc", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Giriş", "main")

if authentication_status == None:
    st.warning("Lütfen Kullanıcı Adınızı ve Şifrenizi Giriniz")
if authentication_status == False:
    st.error("Kullanıcı ismi veya şifre yanlış girilmiştir.")
if authentication_status==True:
    authenticator.logout("Çıkış Yap", "main")
    #Menu Type1
    #############################################################
    ######           Configuration of SideBar             #######
    st.sidebar.title(f"Hoşgeldin {name}")
    with st.sidebar:
        page = option_menu("Menü", ["Ana Sayfa", "Talep Analizi", "SLA Süre Analizi"],
            icons=['house', 'list-task', "gear"], menu_icon="cast", default_index=0)
    #Menu Type2#
    #page = option_menu(None, ["Home Page", "Detailed Request Analysis", "Sla Duration Analysis", 'Sweetviz Report'],
    #    icons=['house', 'cloud-upload', "list-task", 'gear'],
    #    menu_icon="cast", default_index=0, orientation="horizontal")
    #    page

    #############################################################
    ######                   Import Dataset               #######

    dataset=st.container()
    with dataset:
        datasource = 'Anaveri.xlsx'
        sheet_n1 = 'Combined_Dataset'
        df1 = pd.read_excel(datasource, sheet_name=sheet_n1, usecols='A:Q', header=0)

        datasource = 'Anaveri.xlsx'
        sheet_n2 = 'Additional_Dataset'
        df2 = pd.read_excel(datasource, sheet_name=sheet_n2, usecols='A:B', header=0)

        #---
        Sınıf_Tipi = df1['Sınıf_Tipi'].unique().tolist()
        Modül_Tipi = df1['Modül_Tipi'].unique().tolist()

        closereqdf = df1[df1["Talep_Durumu"] == 'Kapalı']
        openreqdf = df1[df1.Talep_Durumu == 'Açık']
        ore=openreqdf["Talep_Durumu"].value_counts()
        cre=closereqdf["Talep_Durumu"].value_counts()
        dfyeni=pd.DataFrame()
        dfyeni=pd.concat([ore,cre],axis=0)
        dfyeni=pd.DataFrame(dfyeni,columns=["Talep_Durumu"])

    with st.sidebar:
        uploaded_file = st.file_uploader("Veriyi değiştirmek için .xlsx dosyası yükle")
        if uploaded_file:
            sheet_n1 = 'Combined_Dataset'
            df11 = pd.read_excel(uploaded_file, sheet_name=sheet_n1, usecols='A:Q', header=0)
            sheet_n2 = 'Additional_Dataset'
            df22 = pd.read_excel(uploaded_file, sheet_name=sheet_n2, usecols='A:B', header=0)


    #############################################################
    ######              Configuration of Main Page       #######
    if page=="Ana Sayfa":
        # Inserted Animation #
        lottie_coding = load_lottiefile("Animasyonlar/70106-website-performance.json")
        st_lottie(lottie_coding,speed=1,loop=True)
        #lottie_hello = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_ye2v3dmd.json")
        #st_lottie(lottie_hello, speed=1, reverse=False, loop=True, quality="low", height=None, width=None, key=None)

        # Inserted Progress Bar #
        st.caption("Yükleniyor")
        bar = st.progress(50)
        for percent_complete in range(100):
            time.sleep(0.00001)
            bar.progress(percent_complete + 1)
        #st.balloons()
        st.success('Tamamlandı')

        #Inserted an Image#
        #st.image("/Users/eceaks/PycharmProjects/streamlite/img0.jpg")

        #Inserted Title, Header
        st.markdown("<h1 style='text-align:center;'>YENİ NESİL TEKNOLOJİLER</h1>",unsafe_allow_html=True)
        st.title("""İstek Performans Raporu""")

        #Insert Caption
        st.caption("Analizler BTYP Raporları kullanılarak oluşturulmuştur.")
        st.subheader("İstek Raporu (Btyp & Tableu Entegre) ")
        st.caption("Projeye Bağlanmamış Uygulama Destek Taleplerinin Detay Raporudur.")

        #Inserted Dataset
        st.write(df1)

        #---#
        st.header("Talep Durum Dağılımı")
        st.caption("""Pasta Grafiği Analizi""")
        tab1,tab2=st.tabs(["Versiyon 1","Versiyon 2"])
        with tab1:
            st.write("Versiyon 1 Tipi Grafik")
            pie_chart = px.pie(df2, values='#ofRequest', names="RequestType")
            st.plotly_chart(pie_chart)
        with tab2:
            st.write("Versiyon 2 Tipi Grafik")
            valuec = df1["Talep_Durumu"].value_counts()
            fig, ax = plt.subplots()
            ax.pie(valuec, autopct='%0.2f%%', labels=['Açık', 'Kapalı'])
            st.pyplot(fig)
        #Inserted an Expander
        with st.expander("Detayları Görmek için Tıklayınız"):
            st.dataframe(valuec)
        #---#

        st.header("Talep Tipi Dağılımı")
        rec=df1["İstek_Tipi_Detay"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(rec, autopct='%0.2f%%', labels=['Hata', 'Yeni İstek', 'İyileştirme/Değişiklik'])
        st.pyplot(fig)
        #Inserted an Expander
        with st.expander("Detayları Görmek için Tıklayınız"):
            st.dataframe(rec)
        #---#

        #Download Dataset as csv file#
        #---#
        st.subheader("Raporu İndir")
        csv = convert_df(df1)
        st.write(emoji.emojize('İstek Raporu (Btyp & Tableu Entegre) :receipt:'))
        st.download_button(
            label="CSV dosyası indir",
            data=csv,
            file_name='btyp_data.csv',
            mime='text/csv',
        )
        #---#

    elif page == "Talep Analizi":

        #Inserted Animation
        lottie_coding = load_lottiefile("Animasyonlar/87792-analysis.json")
        #lottie_hello = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_je2kc06t.json")
        st_lottie(lottie_coding, speed=1, reverse=False, loop=True, quality="low", height=None, width=None, key=None)

        #Inserted a timer
        with st.spinner("Yükleniyor"):
            time.sleep(2)

        st.title("Detaylı Talep Analizi")
        # ---#
        st.subheader('Talep Sınıfları')
        for i in Sınıf_Tipi:
            st.markdown("""
                    #### <span style="color:blue">{temp1}</span> <span style="font-size:12pt">{temp}</span>  """.format(
                temp1="*", temp=i), unsafe_allow_html=True)

        #Inserted expander
        with st.expander("Görmek için Tıkla -> Her Sınıf Tipi İçin Talep Sayısı"):
            st.write(df1["Sınıf_Tipi"].value_counts())
        #---#

        st.subheader('Talep Modülleri')
        for i in Modül_Tipi:
            st.markdown("""
                    #### <span style="color:green">{temp1}</span> <span style="font-size:12pt">{temp}</span>  """.format(
                temp1="*", temp=i), unsafe_allow_html=True)
        with st.expander("Görmek için Tıkla -> Her Modül Tipi İçin Talep Sayısı"):
            st.write(df1["Modül_Tipi"].value_counts())

        # ---#
        tabv1,tabv2=st.tabs(["Sınıf Tipi","Modül Tipi"])
        with tabv1:
            #---------
            st.subheader("Her Sınıf Tipinden Gelen Talep Sayısı")
            a=df1['Sınıf_Tipi'].value_counts().reset_index()
            a=pd.DataFrame(a)
            a.columns =['Sınıf_Tipi', 'NumberofRequest']
            pie_chart2 = px.pie(a, title='Talep Dağılımı', values=a['NumberofRequest'], names='Sınıf_Tipi')
            st.plotly_chart(pie_chart2)
        with tabv2:
            st.header("Her Modül Tipinden Gelen İstek Sayısı")
            b = df1['Modül_Tipi'].value_counts().reset_index()
            b = pd.DataFrame(b)
            b.columns = ['Modül_Tipi', 'NumberofRequest']
            pie_chart3 = px.pie(b, title='Her Modül için Talep Dağılımı', values=b['NumberofRequest'], names='Modül_Tipi')
            st.plotly_chart(pie_chart3)
        #---#
        st.subheader("Tüm Taleplerin Sınıf & Modül Dağılımı")
        tab1, tab2 = st.tabs(["Sınıf Tipi","Modül Tipi"])
        with tab1:
            st.write("Sınıf Tipi / Talep Sayısı")
            Sınıf_Tipi_nmbr = pd.DataFrame(df1['Sınıf_Tipi'].value_counts())
            st.bar_chart(Sınıf_Tipi_nmbr)
        with tab2:
            st.write("Modül Tipi / Talep Sayısı")
            Modül_Tipi_nmbr = pd.DataFrame(df1['Modül_Tipi'].value_counts())
            st.bar_chart(Modül_Tipi_nmbr)
        # ---#
        st.subheader("Modül Tiplerine göre Kapalı & Açık Taleplerin Dağılımı")
        tab1, tab2 = st.tabs(["Kapalı Talepler","Açık Talepler"])
        with tab1:
            st.write("Modül Tipi / Kapalı Talep Sayısı")
            closereqdf = df1[df1.Talep_Durumu == 'Kapalı']
            Modül_Tipi_nmbr_cr = pd.DataFrame(closereqdf['Modül_Tipi'].value_counts())
            st.bar_chart(Modül_Tipi_nmbr_cr)
        with tab2:
            st.write("Modül Tipi / Açık Talep Sayısı")
            openreqdf = df1[df1.Talep_Durumu == 'Açık']
            Modül_Tipi_nmbr_or = pd.DataFrame(openreqdf['Modül_Tipi'].value_counts())
            st.bar_chart(Modül_Tipi_nmbr_or)

            # Detailed Pie CHart Anaylsis
            st.subheader("Detay Analizler")
            path = st.multiselect("Değişken Seçimi:", (
                'Talep_Durumu', 'İstek Sahibi', 'Talep_Sorumlusu', 'Request_Manager', 'Şirket', 'Istek_Tipi', 'İstek_Tipi_Detay',
                'Sınıf_Tipi', 'Modül_Tipi'))
            fig = px.sunburst(data_frame=df1, path=path)
            st.plotly_chart(fig)
        #---#

        st.subheader("Talep Detay İnceleme")
        tab1, tab2, tab3 = st.tabs(["Talep Sahibi Dağılımı", "Talep Sorumlusu Dağılımı","Şirket Dağılımı"])
        with tab1:
            st.header("Talep Sahibi Dağılımı")
            talepsahibi = pd.DataFrame(df1['Talep_Sahibi'].value_counts())
            st.bar_chart(talepsahibi)
            with st.expander("Detaylı İncelemek için"):
                st.write(talepsahibi)
        with tab2:
            st.header("Talep Sorumlusu Dağılımı")
            talepsorumlusu = pd.DataFrame(df1['Talep_Sorumlusu'].value_counts())
            st.bar_chart(talepsahibi)
            with st.expander("Detaylı İncelemek için"):
                st.write(talepsorumlusu)
        with tab3:
            st.header("Şirket Dağılımı")
            talepsirketi = pd.DataFrame(df1['Şirket'].value_counts())
            st.bar_chart(talepsirketi)
            with st.expander("Detaylı İncelemek için"):
                st.write(talepsirketi)


    elif page == "SLA Süre Analizi":
        #---#
        lottie_coding = load_lottiefile("Animasyonlar/81231-time-go.json")
        #lottie_hello = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_eIXuIz.json")
        st_lottie(lottie_coding, speed=1, reverse=False, loop=True, quality="low", height=None, width=None, key=None)

        #Waiting time
        with st.spinner("wait"):
            time.sleep(1)

        st.title("SLA Süre Analizi")
        st.subheader("Her Sınıf Tipi için SLA Süre Analizi ")
        tab1, tab2 = st.tabs(["Versiyon 1", "Versiyon 2"])

        # ---#
        # Box Plot Version 1
        with tab1:
            chart2 = ('RPA', 'ZES EV IOT', 'MOBİL UYGULAMALAR', 'INTRANET SİTELERİ', 'Optimizasyon Portali')
            chart_selection2 = st.selectbox("Sınıf Tipi Seçin1", chart2)
            dataf2rpa = df1[df1["Sınıf_Tipi"] == chart_selection2]

            fig=px.box(data_frame=dataf2rpa, x="Sınıf_Tipi", y="Sla_Süresi", color="Sınıf_Tipi")
            st.plotly_chart(fig)
        #---#
        # Box Plot Version 2
        with tab2:
            chart = ('RPA', 'ZES EV IOT', 'MOBİL UYGULAMALAR', 'INTRANET SİTELERİ', 'Optimizasyon Portali')
            chart_selection = st.selectbox("Sınıf Tipi Seçin2", chart)
            fig, ax = plt.subplots()

            if chart_selection == 'RPA':
                datafrpa = df1[df1["Sınıf_Tipi"] == 'RPA']
                sns.boxplot(x="Sınıf_Tipi", y="Sla_Süresi", data=datafrpa, ax=ax)
            elif chart_selection == 'ZES EV IOT':
                datafzes = df1[df1["Sınıf_Tipi"] == 'ZES EV IOT']
                sns.boxplot(x="Sınıf_Tipi", y="Sla_Süresi", data=datafzes, ax=ax)
            elif chart_selection == 'MOBİL UYGULAMALAR':
                datafmobil = df1[df1["Sınıf_Tipi"] == 'MOBİL UYGULAMALAR']
                sns.boxplot(x="Sınıf_Tipi", y="Sla_Süresi", data=datafmobil, ax=ax)
            elif chart_selection == 'INTRANET SİTELERİ':
                datafintra = df1[df1["Sınıf_Tipi"] == 'INTRANET SİTELERİ']
                sns.boxplot(x="Sınıf_Tipi", y="Sla_Süresi", data=datafintra, ax=ax)
            elif chart_selection == 'Optimizasyon Portali':
                datafoptim = df1[df1["Sınıf_Tipi"] == 'Optimizasyon Portali']
                sns.boxplot(x="Sınıf_Tipi", y="Sla_Süresi", data=datafoptim, ax=ax)
            st.pyplot(fig)

        #---#
        st.subheader("Talep vs SLA Süresi")
        unique_Sla_Süresi = df1['Sla_Süresi'].unique().tolist()
        moduleselect=st.slider('Sla Süresi', min_value=min(unique_Sla_Süresi),max_value=max(unique_Sla_Süresi),value=(min(unique_Sla_Süresi),max(unique_Sla_Süresi)))

        typeofmodul=st.multiselect('Birden Fazla Sınıf Tipi Seçebilirsiniz',Sınıf_Tipi, default=Sınıf_Tipi)
        tryout=(df1["Sla_Süresi"].between(*moduleselect))& (df1['Sınıf_Tipi'].isin(typeofmodul))
        number_of_result=df1[tryout].shape[0]
        st.markdown(f'*Belirlenmiş Sla Süresi Aralığında Bulunan Mevcut Talep sayısı : {number_of_result}*' )

        #---#
        # Scatter Plot
        st.subheader("Sla Süresi / Talep Numarası")
        st.write("Opsiyonlar: Sınıf Tipi, Modül Tipi, Talep Tipi")
        tab1, tab2 = st.tabs(["Versiyon 1", "Versiyon 2"])
        # Version 1 Scatter Plot
        with tab1:
            selectopt = st.selectbox('Kategori Seçimi', ("Sınıf_Tipi", "Modül_Tipi", "İstek_Tipi_Detay"))
            fig = px.scatter(data_frame=df1, x='Talep_Numarası', y="Sla_Süresi", color=selectopt)
            st.plotly_chart(fig)
        #Versiyon 2 Scatter Plot
        with tab2:
            fig, ax = plt.subplots()
            cat_cols = df1.select_dtypes(include=['object']).columns.tolist()
            cat_cols = ['Talep_Durumu', 'İstek_Tipi_Detay',
                        'Sınıf_Tipi', 'Modül_Tipi']
            hue_type = st.selectbox("check", cat_cols)
            sns.scatterplot(x='Talep_Numarası', y='Sla_Süresi', hue=hue_type, ax=ax, data=df1)
            st.pyplot(fig)
        # ---#

        #Summary Table
        st.subheader('Talep Tarihi/Sla Süresi/Sınıf Tipi')
        fig = go.Figure(data=go.Table(
            header=dict(values=list(df1[['Talep_Açılış_Tarihi', "Talep_Numarası", 'Sla_Süresi', 'Sınıf_Tipi']].columns),
                        fill_color='#FD8E72', align='center'),
            cells=dict(values=[df1.Talep_Açılış_Tarihi, df1.Talep_Numarası, df1.Sla_Süresi, df1.Sınıf_Tipi], fill_color='#E5ECF6',
                       align='left')))
        # fig.update_layout()
        st.write(fig)
        # ---#

        #---#
        st.header("Talep Yoğunluğu")
        st.write(emoji.emojize(':chart_increasing:'))
        line = pd.DataFrame(df1['Talep_Açılış_Tarihi'].value_counts())
        st.bar_chart(line)
        with st.expander("Detaylı İncelemek için"):
            st.write(line)

        # Inserted Animation
        # lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ncztkceu.json")
        lottie_coding = load_lottiefile(
            "Animasyonlar/72879-customer-support-help-support-agent.json")
        st_lottie(lottie_coding, speed=1, reverse=False, loop=True, quality="low", height=None, width=None,
                  key=None)



    #elif page=="Sweetviz Raporu":
    #    st.title("Sweetviz Raporu")
    #    st.write("Otomatik Rapor Çıktısı")

        #Inserted Progress Bar
    #    st.caption("Yükleniyor")
    #    bar = st.progress(50)
    #    for percent_complete in range(100):
    #        time.sleep(0.00001)
    #        bar.progress(percent_complete + 1)
    #    st.success('Tamamlandı')

    #    st.write(emoji.emojize('Check it from the next tab :thumbs_up:'))
    #    my_report = sv.analyze(df1)
    #    my_report.show_html()


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