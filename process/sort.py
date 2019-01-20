import pandas as pd
import os
def sort2txt():
    df=pd.read_csv('test.csv',sep='\t',names=['time','content','authid','url','source'])
    df['time']=pd.to_datetime(df['time'],format='%Y_%m_%d_%H_%M_%S') 
    #df.index = df['time']
    #del df['time']
    df = df.sort_values(by = 'time')
    #df = df["content"].dropna()
    NONE_VIN = (df["content"].isnull()) | (df["content"].apply(lambda x: str(x).isspace()))

    df = df[~NONE_VIN]
    df1=df['content']
    df.to_csv(os.getcwd()+"\\"+'sorted.csv',sep='\t',header=None,index=None)
    df1.to_csv(os.getcwd()+"\\"+'sorted.txt',sep='\t',header=None,index=None)
    return os.getcwd()+"\\"+'sorted.txt'