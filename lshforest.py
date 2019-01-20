from datasketch import MinHashLSHForest, MinHash
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer 
from math import log
import pandas as pd
import numpy as np
import datetime


def delspace():
	f=open('.\\data\\afterFenci_sorted.txt', 'r',encoding='utf-8',errors='ignore')
	lines=f.readlines()
	flag=[]
	count=0
	for line in lines:
		line=line.replace(' ','')
		if(len(line)!=0):
			flag.append(count)
		count=count+1
	f2=open('.\\data\\afterFenci_sorted2.txt', 'w+',encoding='utf-8',errors='ignore')
	for i in flag:
    		f2.write(lines[i])

	f3=open('.\\data\\sorted.csv', 'r',encoding='utf-8',errors='ignore')
	lines2=f3.readlines()
	f4=open('.\\data\\sorted2.csv', 'w+',encoding='utf-8',errors='ignore')
	for i in flag:
    		f4.write(lines2[i])
	
def mylshforest(corpus):
	print(len(corpus))
	forest = MinHashLSHForest(num_perm=32)
	score_res=[0]
	mh=[]
	for i in range(len(corpus)-1):
		doc=corpus[i]
		doc2=corpus[i+1]
		m=MinHash(num_perm=32)
		for d in doc:
			m.update(d.encode('utf8'))
		forest.add(str(i),m)
		forest.index()
		mh.append(m)
		
		m2=MinHash(num_perm=32)
		for d in doc2:
			m2.update(d.encode('utf8'))
		result = forest.query(m2, 10)
		score=0.0
		for j in range(len(result)):
			score=score+m2.jaccard(mh[int(result[j])])
		if(len(result)>0):
			score=score/len(result)
		score_res.append(score)
		i=i+1
	return score_res
	
def calres_big():

	starttime = datetime.datetime.now()
	file='.\\data\\afterFenci_sorted2.txt'
	#vectorizer=CountVectorizer(token_pattern='[\u4e00-\u9fa5_a-zA-Z0-9]{1,}')
	f=open(file, 'r',encoding='utf-8',errors='ignore')
	f2=open('.\\data\\lshres.csv', 'w+',encoding='utf-8',errors='ignore')
	#corpus=f.readlines()
	vectorizer=HashingVectorizer(n_features = 300,norm = None,token_pattern='[\u4e00-\u9fa5_a-zA-Z0-9]{1,}')
	corpus=f.readlines()
	
	weight=[]
	sum_doc=len(corpus)
	sum_word=0
	for doc in corpus:
		sum_word+=len(doc)
	avg_word=(sum_word/sum_doc)
	for i in range(sum_doc):
		tmp=len(corpus[i])/avg_word
		weight.append(tmp)
		
	#print (vectorizer.fit_transform(corpus))
	vec=vectorizer.transform(corpus).toarray()
	hash_corpus=[]
	for i in range(len(vec)):
		tmp=[]
		for j in range(len(vec[i])):
			tmp.append(str(vec[i][j]))
		hash_corpus.append(tmp)
	#print(hash_corpus)
				
	fs=mylshforest(hash_corpus)
	#print(fs)
	hash_corpus2=list(reversed(hash_corpus))
	bs=mylshforest(hash_corpus2)
	bs2=list(reversed(bs))
	#print(bs2)
	final_res=[]
	count=0
	for i in range(len(fs)):
		f=(bs2[i]/(fs[i]+1))*weight[count]
		final_res.append(f)
		count=count+1
	for x in final_res:
		x = float(x - np.min(final_res))/(np.max(final_res)- np.min(final_res))
		x=x*100
		f2.write('%.2f' %x)
		f2.write('\n')
	endtime = datetime.datetime.now()
	print( (endtime - starttime).seconds )
	
	
def calres_small():

	starttime = datetime.datetime.now()
	file='.\\data\\afterFenci_sorted2.txt'
	vectorizer=CountVectorizer(token_pattern='[\u4e00-\u9fa5_a-zA-Z0-9]{1,}')
	f=open(file, 'r',encoding='utf-8',errors='ignore')
	f2=open('.\\data\\lshres.csv', 'w+',encoding='utf-8',errors='ignore')
	corpus=f.readlines()
	
	weight=[]
	sum_doc=len(corpus)
	sum_word=0
	for doc in corpus:
		sum_word+=len(doc)
	avg_word=(sum_word/sum_doc)
	for i in range(sum_doc):
		tmp=len(corpus[i])/avg_word
		weight.append(tmp)		
	
	fs=mylshforest(corpus)
	#print(fs)
	corpus2=list(reversed(corpus))
	bs=mylshforest(corpus2)
	bs2=list(reversed(bs))
	#print(bs2)
	final_res=[]
	count=0
	for i in range(len(fs)):
		f=(bs2[i]/(fs[i]+1))*weight[count]
		final_res.append(f)
		count=count+1
	for x in final_res:
		x = float(x - np.min(final_res))/(np.max(final_res)- np.min(final_res))
		x=x*100
		f2.write('%.2f' %x)
		f2.write('\n')
		count=count+1
	endtime = datetime.datetime.now()
	print( (endtime - starttime).seconds )