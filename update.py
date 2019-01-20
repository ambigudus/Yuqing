import pandas as pd 
import csv
from elasticsearch import Elasticsearch
from elasticsearch import helpers

def ImportVlue(k,i,_index,_type):

	action={
        "_index":_index,
        "_type":_type,
        "_id":i,
        "_source":{
			#"keyword" : k['keyword'],
			#"n_comment" : k['n_comment'],
			"time" : k[0],
			"content" : k[1],            
			"authid" : k[2],
			#"sentiment" : k['sentiment'],
			#"n_like" : k['n_like'],
			#"n_forward" : k['n_forward'],
			"url" : k[3],
			#"attention" : k['attention'],
			#"create_time" : k['create_time'],
			"source" : k[4],
			"score": round(float(k[5]),6)
            }
        }

	return action
'''
def create(_type):
    mappings = {
                "mappings": {
                    _type: {                           #type_doc_test为doc_type
                        "properties": {
                            "time": {
                                "type": "text",
                                #"format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                                
                            },
                            "content": {
                                "type": "text",

                            },
                            "authid": {
                                "type": "keyword",  # keyword不会进行分词,text会分词
 
                            },
                            "url": {
                                "type": "keyword",
                                "index": False
                            },
                            "source": {
                                "type": "keyword",
                                "index": True
                            },

                            "innovation": {
                                "type": "float"
                                
                            }
                        }
                    }
                }
            }
    return mappings

'''
def Update(filename='final'):
    es = Elasticsearch(hosts=[{'host':'127.0.0.1','port':9200}])

    _index = filename
    _type = 'output'
    es.indices.delete(index=_index, ignore=[400, 404])
    #es.indices.create(index = _index,body =create(_type))
    #f=pd.read_csv(os.getcwd()+"\\"+file,sep = '\s')
    with open('.\\data\\final.csv',encoding='utf-8') as f: 
        actions=[]
        reader=csv.reader(f,delimiter = '\t')
        i=1
        for line in reader:
            action=ImportVlue(line,i,_index,_type)
            
            actions.append(action)
            i+=1
            if(len(actions)==500):
                helpers.bulk(es, actions)
                del actions[0:len(actions)]

        if (len(actions) > 0):
            helpers.bulk(es, actions)
        print('处理共'+str(i)+'条数据')

if __name__=='__main__':
    Update()
