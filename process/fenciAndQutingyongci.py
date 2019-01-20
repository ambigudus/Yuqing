# -*- coding:utf-8 -*-
import jieba
import sys
import datetime


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',encoding='utf-8').readlines()]
    return stopwords


def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('Mystopwords.txt')
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr


def fenci():
	begin = datetime.datetime.now()
	inputs = open('sorted.txt', 'r',encoding='utf-8')
	outputs = open('afterFenci_sorted.txt', 'w',encoding='utf-8') 
	#start=0
	for line in inputs:
		# if start>=100000:
			# break
		# start=start+1
		line_seg = seg_sentence(line)
		outputs.write(line_seg + '\n')
	outputs.close()
	inputs.close()
	end = datetime.datetime.now()

if __name__=='__main__':
	fenci();
