
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import re
import os

def GetVlue():
	es1 = Elasticsearch(hosts=[{'host':'114.212.189.141','port':30011}])
	query ={
	"query": {"match_all": {}}
	}
	scanResp = helpers.scan(client=es1, query=query, scroll="5m", index='crawler', timeout="5m")
	for k in scanResp:
		yield k
def ImportVlue(i,k):
	k=dict(k)
	#print(len(k['_source']))
	action={
        "_index":"yuqingdata",
        "_type":"yuqing",
        "_id":i,
        "_source":{
			#"keyword" : k['_source']['keyword'],
			#"n_comment" : k['_source']['n_comment'],
			"time" : k['_source']['time'],
			"authid" : k['_source'].get('authid','None'),
			#"sentiment" : k['_source']['sentiment'],
			#"n_like" : k['_source']['n_like'],
			#"n_forward" : k['_source']['n_forward'],
			"url" : k['_source']['url'],
			#"attention" : k['_source']['attention'],
			#"create_time" : k['_source']['create_time'],
			"source" : k['_source']['source'],
			"content" : k['_source']['content'] ,
			"innovation": 0
            }
        }

	return action

def write_file(k,filename):
	with open(filename,'a',encoding='utf-8',errors='ignore') as f:
		k=dict(k)
		if re.match(r'\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}',k['_source']['time']): 
			a=re.compile('<.*>')
			tmp=re.sub(r'\t|\n|\r| ','',k['_source']['content'])
			tmp=a.sub('',tmp)
			f.write(k['_source']['time'])
			f.write('\t')
			f.write(tmp)
			f.write('\t')
			f.write(k['_source'].get('authid','None'))
			f.write('\t')	
			f.write(k['_source']['url'])
			f.write('\t')	
			f.write(k['_source']['source'])			
			f.write('\n')


def crawler(filename='.\\data\\test.csv',sum=10000):
	#es2 = Elasticsearch(hosts=[{'host':'127.0.0.1','port':9200}])
	list1 = GetVlue()
#	actions=[]
	count=0
	for i,k in enumerate(list1,1):
		k=dict(k)
		if re.match(r'\d{4}_\d{2}_\d{2}_\d{2}_\d{2}_\d{2}',k['_source']['time']):
			write_file(k,os.getcwd()+"\\"+filename)
			# action=ImportVlue(i,k)
			# print('正在处理'+str(i)+'条数据')
			# actions.append(action)
			# if(len(actions)==500):
			# 	helpers.bulk(es2, actions)
			# 	del actions[0:len(actions)]
			if (i+1)%5000==0:
				print('爬取第%d条'%(i+1))
			if count==sum-1:
				print('爬取完毕，共%d条'%sum)
				break
			count+=1
	
	# if (len(actions) > 0):
	# 	helpers.bulk(es2, actions)


# filename=input('输入本地csv文件名：')
# crawler(filename)