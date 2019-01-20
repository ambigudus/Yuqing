import pandas as pd 
import csv
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import pandas as pd

def ImportVlue(k,i,_index,_type):

	action={
        "_index":_index,
        "_type":_type,
        "_id":i,
        "_source":{
			#"keyword" : k['keyword'],
			#"n_comment" : k['n_comment'],
			"time" : k[0],
			"authid" : k[2],
			#"sentiment" : k['sentiment'],
			#"n_like" : k['n_like'],
			#"n_forward" : k['n_forward'],
			"url" : k[3],
			#"attention" : k['attention'],
			#"create_time" : k['create_time'],
			"source" : k[4],
			"content" : k[1] ,
			"innovation": k[5]
            }
        }

	return action

def Update():
    es = Elasticsearch(hosts=[{'host':'127.0.0.1','port':9200}])
    #print("数据格式：time authid url source content,Tab分开")
    #file = input("输入文件名：")
    _index = input('自定义_index：')
    _type = input('自定义_type:')
    #f=pd.read_csv(os.getcwd()+"\\"+file,sep = '\s')
    with open('final.csv',encoding='utf-8') as f: 
        actions=[]
        reader=csv.reader(f,delimiter = '\t')
        i=1
        for line in reader:

            action=ImportVlue(line,i,_index,_type)
            print('正在处理'+str(i)+'条数据')
            actions.append(action)
            i+=1
            if(len(actions)==500):
                helpers.bulk(es, actions)
                del actions[0:len(actions)]

        if (len(actions) > 0):
            helpers.bulk(es, actions)