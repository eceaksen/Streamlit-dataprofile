import numpy as np
import pandas as pd

label_list=['ece','efe','derya']
data_list=[10,20,30]
pd.Series(data=data_list,index=label_list)
pd.Series(data_list)

npArray=np.array([10,20,30])
pd.Series(npArray)
pd.Series(npArray,label_list)

pd.Series(dataDict)

#İki seri toplama işlemiyle birleştirilebilir
ser1=pd.Series([2,12,12,6],["b","e","a","k"])
total=ser1+ser2
total["b"]

#session2
from numpy.random import randn

randn(3,3)
df=pd.DataFrame(data=randn(3,3),index=["a","b","c"],columns=["c1","c2","c3"])

df["c2"]
df.loc["a"] #satır bilgilerine erişmek için kullanılır

df[["c1","c2"]]#df parçalar

#sütun ekleme
df["c4"]=pd.Series(randn(3),["a","b","c"])
df


df["c5"]=df["c1"]+df["c2"]
df.drop("c5")
#axis kavramı: yatay axis 0, dikey1
#axis 0'a göre arar drop komutu kullanıldığında default değeri 0
#yapılan işlemlerin yansıması için inplace=True olarak değişmeli default olarak false gelır
df.drop("c5",axis=1,inplace=False,inplace=True)

df.iloc[0] #df.loc["a"] aynı şeeyi verir
df.loc["a","c1"]
df.loc[["a","b"],["c1","c2"]]

#session2-Filtering

import numpy.random import randn

df=pd.DataFrame(randn(4,3),["a","b","c","d"],["c1","c2","c3","c4"])

df>-1
booleandf=df>0
df[booleandf] #true değerler kalacak false değerler na olarak değişecek

df[df>0] #alternatif yazım

df["c1"]>0
df[df["c1"]>0] #a satır indexindeki değer negatifti dolayısıyla o satırı komple kaldırdı

df[(df["c1"]>0) & df["c2"]>0]#iki kosuluda sağlayan gelir

df["c5"]=pd.Series(randn(4),["a","b","c","d"])#yeni sütun eklendi
df["c5"]=randn(4)

df["c6"]=["1","2","3","4"]
df.set_index("c6", inplace=True) #A, B, C, D yerine sütun 5 geçti, df değişmesi için true yaz
df.index.names#row index ismi ne onu bulduk