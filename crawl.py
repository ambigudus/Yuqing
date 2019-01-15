
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import re

def GetVlue():
  es = Elasticsearch(hosts=[{'host':'114.212.189.141','port':30011}])
  query ={
    "query": {"match_all": {}}
  }
  scanResp = helpers.scan(client=es, query=query, scroll="3m", index='crawler', timeout="3m")
  for k in scanResp:
    yield k
 
def write_file(k):
  with open('E:\\statics2.csv','a',encoding='utf-8',errors='ignore') as f:
    k=dict(k)
    a=re.compile('\<.*\>')
    tmp=k['_source']['content'].replace("\n", "")
    tmp=a.sub('',tmp)
    f.write(k['_source']['time'])
    f.write(',')
    f.write(tmp)


    f.write('\n')


if __name__=="__main__":
  list1 = GetVlue()
  for index,k in enumerate(list1,1):
    write_file(k)

    print('正在导出'+str(index)+'条数据')
