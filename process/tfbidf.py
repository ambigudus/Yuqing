from sklearn.feature_extraction.text import CountVectorizer
from math import log
import pandas as pd
def tf(word,doc):
	all_num=sum([doc[key] for key in doc])
	return float(doc[word])/all_num

def idf(word,doc_list):
	all_num=len(doc_list)
	word_count=0
	for doc in doc_list:
		if word in doc:
			word_count+=1
	if all_num==0:
		return 0
	return log(float(all_num)/(word_count+1))

def tfidf(word,doc,doc_list):
	score=tf(word,doc)*idf(word,doc_list)
	return score

def tfbidf(word,doc,doc_list,index):
	doc_len=len(doc_list)
	before_doc=doc_list[:index]
	score=tf(word,doc)*idf(word,before_doc)
	return score

def norm(dic):
	#print(dic)
	sum=0.0
	for i in dic:
		sum+=dic[i]
	for i in dic:
		if sum==0:
			break
		dic[i]=dic[i]/sum

def calP(dic1,dic2):
	res=0.0
	norm(dic1)
	norm(dic2)
	for i in dic1:
		if i in dic2:
			res=res+dic1[i]*dic2[i]
	return res

def calBS(doc,doc_list,t,index):
	res=0.0
	dic1={}
	before_doc=[]
	if index < t:
		before_doc=doc_list[:index]
	else :
		before_doc=doc_list[index-t:index]
	index2=1
	for doc2 in before_doc:
		for word in doc:
			dic1.update({word:tfbidf(word,doc,doc_list,index-len(before_doc)+index2-1)})
		dic2={}
		for word2 in doc2:
			dic2.update({word2:tfbidf(word2,doc2,doc_list,index-len(before_doc)+index2-1)})
		res=res+calP(dic1,dic2)
		#print(calP(dic1,dic2))
		index2=index2+1
	return res

def calFS(doc,doc_list,t,index):
	#print(index)
	res=0.0
	dic1={}
	for word in doc:
		dic1.update({word:tfbidf(word,doc,doc_list,index)})
	before_doc=[]
	if index+t >= len(doc_list):
		before_doc=doc_list[index+1:]
	else :
		before_doc=doc_list[index+1:index+t+1]
	#index2=1
	#print(len(doc_list))
	for doc2 in before_doc:
		dic2={}
		for word2 in doc2:
			dic2.update({word2:tfbidf(word2,doc2,doc_list,index)})
		res=res+calP(dic1,dic2)
		#print(calP(dic1,dic2))
		#index2=index2+1
	#print(res)
	return res

def calculate():
	print('start')

	vectorizer=CountVectorizer(token_pattern='[\u4e00-\u9fa5_a-zA-Z0-9]{1,}')
	f=open('afterFenci_sorted.txt', 'r',encoding='utf-8',errors='ignore')
	corpus=f.readlines()
	vec=vectorizer.fit_transform(corpus).toarray()
	print(vec)
	dic=vectorizer.get_feature_names()
	start=0
	doc_list=[]
	print('start2')
	for i in vec:
		doc={}
		num=0
		for j in i:
			if j>0:
				doc.update({dic[num]:float(j)})
			num=num+1
		doc_list.append(doc)
		#print('here')
	i_num=1
	print('begin2')
	f2 = open('result.csv', 'w',encoding='utf-8')
	for doc in doc_list:
		if calBS(doc,doc_list,10,i_num)!=0:
			# f2.write('%d         ' % i_num)
			# f2.write('%f   ' %(calFS(doc,doc_list,100,i_num)/calBS(doc,doc_list,100,i_num)))
			# f2.write('%f   ' %(calFS(doc,doc_list,100,i_num)))
			# f2.write('%f   ' %(calBS(doc,doc_list,100,i_num)))
			f2.write('%f' %(calFS(doc,doc_list,10,i_num)/calBS(doc,doc_list,10,i_num)))
			f2.write('\n')
		else:
			tmp=0.0
			f2.write('0.000000')
			f2.write('\n')
		i_num+=1
def merge():
	df1=pd.read_csv('sorted.csv',sep='\t',names=['time','content','authid','url','source'])
	df2=pd.read_csv('result.csv',sep='\t',names=['innovation'])
	df=pd.concat([df1,df2],1)
	df.to_csv('final.csv',sep='\t',header=None,index=None)
