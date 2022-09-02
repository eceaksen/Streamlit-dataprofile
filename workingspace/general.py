df["col"].unique()
df["col"].nunique()
df["col"].value_counts()

df[(df["col1"]>=4) & (df["col2"]==300)]

df["col"].apply()
df.drop("col",axis=1,inplace=True)#sütunu siler

df.index
df.index.name

df.sort_values("col2",ascending=False)
