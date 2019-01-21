# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 13:47:55 2019

@author: houwenxin
"""

from elasticsearch import Elasticsearch

HOST = "114.212.189.141"
#HOST = "172.27.142.174"
PORT = 30011
#PORT = 9200
return_size = 100

class ElasticSearcher():
    def __init__(self, host, port, index):
        self.host = host
        self.port = port
        self.es = Elasticsearch([self.host], port=self.port)
        self.index = index
        
    def structuredSearch(self, srcDict={"authid":"", "time":"", "url":"", "content":""}, sort="desc", rank_type="time"):
        if rank_type == "time": rank_type = rank_type + ".keyword"
        authid = srcDict["authid"]
        time = srcDict["time"]
        url = srcDict["url"]
        content = srcDict["content"]
        return_types = ["_type", "authid", "time", "content", "url", "innovation"]
        dsl = {
                "query": {
                        "bool": {
                                "must": [
                                            { "term": {}}, 
                                            {"prefix":{}},
                                            { "term": {}}, 
                                            { "match":{}}
                                ]
                                  
                        }
                        },
                "sort": [{rank_type: {"order": "desc"}}],
                "_source": return_types
            }
        if authid: dsl["query"]["bool"]["must"][0]["term"]["authid.keyword"] = authid #为了查询中文
        if time: 
            dsl["query"]["bool"]["must"][1]["prefix"]["time.keyword"] = time
            
        if url: dsl["query"]["bool"]["must"][2]["term"]["url"] = url
        if content: dsl["query"]["bool"]["must"][3]["match"]["content"] = content
        if not content: del dsl["query"]["bool"]["must"][3]
        if not url: del dsl["query"]["bool"]["must"][2]
        if not time: del dsl["query"]["bool"]["must"][1]
        if not authid: del dsl["query"]["bool"]["must"][0]
        if not dsl["query"]["bool"]["must"]: dsl = None
        
        return_data = self.es.search(index=self.index, body = dsl, size=return_size, request_timeout=20) # default: 10
        results = []
        for hit in return_data["hits"]["hits"]:
            result = ""
            for return_type in return_types:
                if return_type in hit["_source"]:
                    result = result + str(hit["_source"][return_type]) + "\t"
                else:
                    result = result + "Unknown" + "\t" # 有的数据没有authid
            #result += str(hit["_score"])
            results.append(result)
        
        count_data = self.es.search(index=self.index, request_timeout=20)
        if sort == "desc" and rank_type == "time":
            results.sort(key=lambda x:str(x).split("\t")[1], reverse=True)
        elif sort == "desc" and rank_type == "score":
            results.sort(key=lambda x:str(x).split("\t")[4], reverse=True)
        results.append(count_data["hits"]["total"])
        return results
    """
    def contentSearch(self, content=""):
        return_types = ["authid", "time", "content", "url", "score"]
        dsl = {
                "query": {
                        "match":{
                                "content": content
                                }
                        },
                "_source": return_types
            }
        if not content : dsl = None
        return_data = self.es.search(index=self.index, body = dsl, size=return_size, request_timeout=20)
        results = []
        for hit in return_data["hits"]["hits"]:
            result = ""
            for return_type in return_types:
                if return_type in hit["_source"]:
                    result = result + str(hit["_source"][return_type]) + "\t"
                else:
                    result = result + "Unknown" + "\t" # 有的数据没有authid
            results.append(result)
        return results
    """
    def sortedResult(self, rank_type="time"):
        return_types = ["authid", "time", "content", "url", "score"]
        if rank_type=="time": rank_type = rank_type + ".keyword"
        dsl = {
                "query": {
                        #"match_all": {},
                        "term": {"_type":"weibo"}
                }, 
                "sort": [{rank_type: {"order": "desc"}}]
            }
        return_result = self.es.search(index=self.index, body = dsl, size=return_size, request_timeout=20)
        results = []
        for hit in return_result["hits"]["hits"]:
            result = ""
            for return_type in return_types:
                if return_type in hit["_source"]:
                    result = result + str(hit["_source"][return_type]) + "\t"
                else:
                    result = result + "Unknown" + "\t" # 有的数据没有authid
            results.append(result)
        results.append(return_result["hits"]["total"])
        return results
    
if __name__ == "__main__":
    es = ElasticSearcher(HOST, PORT, "120test")
    #content = "否则要难过死我了"
    #results = es.contentSearch("crawler", content)
    srcDict={"authid":"", "time":"2019-01", "url":"", "content":""}
    results = es.structuredSearch(srcDict)
    for result in results:
        print(result)
        print("-" * 100)
    #results = es.sortedResult()
    #for result in results:
    #    print(result)
    #    print("-" * 100)
    