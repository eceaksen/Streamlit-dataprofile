
import pandas as pd

btyp_data=pd.read_csv('S_data3.csv',index_col=0)
print(btyp_data['Durumu'].value_counts())

st.header("Data")
df = pd.read_csv('/Users/eceaks/PycharmProjects/streamlite/S_data5.csv')
st.write(df.head())  # first 5 entry
# nbr_tickets=btyp_data.count(0)
# print(nbr_tickets)

st.header("Açık Talepler")
    excel_f = '/Users/eceaks/PycharmProjects/streamlite/Açık_req.xlsx'
    sheet_n = 'ar'
    df4 = pd.read_excel(excel_f, sheet_name=sheet_n, usecols='A:N', header=0)
    st.write(df4)
    sheet_n2 = 'summary'
    df5 = pd.read_excel(excel_f, sheet_name=sheet_n2, usecols='A:B', header=0)
    st.write(df5)

"""st.header("dene")
    st.header("Class Type vs #of Request -All Requests")

    st.write(df1['ClassType'].value_counts())
    classtype_nmbr1 = pd.DataFrame(data=df1['ClassType'].value_counts())
    classtype_nmbr1=classtype_nmbr1.set_index().transpose()
    #st.write(classtype_nmbr1)

    st.write(classtype_nmbr1)
    st.bar_chart(classtype_nmbr1)
    #st.bar_chart(classtype_nmbr)"""

p=figure(title='simple')
p.circle("Sla_Duration",y="Istek_Numarası",source=df1)
st.bokeh_chart(p)