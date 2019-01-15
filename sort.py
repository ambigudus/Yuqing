import pandas as pd

df=pd.read_csv('E:\\statics2.csv',names=['time','content'])
df['time']=pd.to_datetime(df['time'],format='%Y_%m_%d_%H_%M_%S') 
df.index = df['time']
del df['time']
df=df.sort_index()
#df = df["content"].dropna()
NONE_VIN = (df["content"].isnull()) | (df["content"].apply(lambda x: str(x).isspace()))

df = df[~NONE_VIN]
df.to_csv('E:\\123.csv',header=None,index=None)
print(df)