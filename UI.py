# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 18:38:03 2019

@author: houwenxin
"""

import tkinter as tk
from tkinter import filedialog
import search

class UI():
    def __init__(self):
        self.index = "crawler"
        
        self.window = tk.Tk()
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight() - 70
    
        self.window.geometry("%dx%d+%d+%d" %(self.width, self.height, 0, 0))
        self.window.resizable(width=0, height=0)
        
        self.window.title('NJUSAS舆情分析系统')
        ##窗口尺寸
        #self.window.geometry('1200x600')
        
        window_width = int(self.width / 42)
        
        tk.Label(text='    作者：    ').grid(row=0,column=0) # 创建标签
        self.entry_authid = tk.Entry(width=window_width) #输入框实例化
        self.entry_authid.grid(row=0,column=1) #输入框
        
        tk.Label(text='    时间：    ').grid(row=0,column=2)
        self.entry_time = tk.Entry(width=window_width)#输入框实例化
        self.entry_time.grid(row=0, column=3) #文件后缀输入框
        
        tk.Label(text='    链接：    ').grid(row=0,column=4)
        self.entry_url = tk.Entry(width=window_width)#输入框实例化
        self.entry_url.grid(row=0, column=5) #文件后缀输入框
        
        tk.Label(text='    内容：    ').grid(row=0,column=6)
        self.entry_content = tk.Entry(width=window_width) #输入框实例化
        self.entry_content.grid(row=0, column=7) #文件后缀输入框
        
        tk.Button(text='   查询（时间序）   ', height=1, width=15, command=lambda:self.search("time")).grid(row=0,column=8,padx=3,sticky=tk.W)#按钮
        tk.Button(text='   上传文件   ', height=1, width=10, command=self.uploadWindow).grid(row=0,column=9,padx=3,rowspan=2,sticky=tk.W)#按钮
        tk.Button(text='   查询（得分序）   ', height=1, width=15, command=lambda:self.search("score")).grid(row=1,column=8,padx=3,sticky=tk.W)#按钮


        self.list_box = tk.Listbox(height=40, width=210)
        self.list_box.grid(row=10, column=0, columnspan=50) #显示列表框
        #yscrollbar = tk.Scrollbar(self.list_box,command=self.list_box.yview).grid(row=10, column=0, sticky=tk.NS)
        self.scrollbar_x = tk.Scrollbar(orient="horizontal")
        self.list_box.configure(xscrollcommand = self.scrollbar_x.set)
        
        self.scrollbar_x.grid(row=11,column=0,columnspan=10,sticky=tk.E + tk.W)
        self.scrollbar_x['command']=self.list_box.xview
        
        self.scrollbar_y = tk.Scrollbar(orient="vertical")
        self.list_box.configure(yscrollcommand = self.scrollbar_y.set)
        
        self.scrollbar_y.grid(row=10,column=10,rowspan=10,sticky=tk.N + tk.S)
        self.scrollbar_y['command']=self.list_box.yview
        ##显示出来
        self.window.mainloop()
    
    def search(self, rank_type="time"):
        searcher = search.ElasticSearcher(search.HOST, search.PORT, index=self.index)
        self.list_box.delete(0, tk.END)
        authid = self.entry_authid.get()
        time = self.entry_time.get()
        url = self.entry_url.get()
        content = self.entry_content.get()
        
        if authid or time or url or content:
            srcDict={"authid":authid, "time":time, "url":url, "content":content}
            results = searcher.structuredSearch(srcDict=srcDict, rank_type=rank_type)
        else:
            results= searcher.sortedResult(rank_type=rank_type)
        total_count = results[-1]
        del results[-1]
        
        self.list_box.insert(tk.END, "本次查询查询到了%d条记录，当前服务器中共有%d条记录。" 
                             %(len(results), total_count))
        self.list_box.insert(tk.END, "\n")
        showList = ["作者", "时间", "内容", "链接", "得分"]
        for result in results:
            resultList = result.split("\t")
            for i in range(len(showList)):
                try:
                    if len(resultList[i]) > 2730:
                        self.list_box.insert(tk.END, showList[i] + "（原文较长，仅显示部分结果）：" + resultList[i][:2730])
                    else:
                        self.list_box.insert(tk.END, showList[i] + "：" + resultList[i])
                except tk.TclError as error: #防止non-BMP Unicode characters的显示错误
                    print('{}. It will be converted.'.format(error))
                    self.list_box.insert(tk.END, showList[i] + self._convert65535(resultList[i]))
            self.list_box.insert(tk.END, "\n")        
            '''
            self.list_box.insert(tk.END, "作者：" + result.split("\t")[0])
            self.list_box.insert(tk.END, "时间：" + result.split("\t")[1])
            self.list_box.insert(tk.END, "内容：" + result.split("\t")[2])
            self.list_box.insert(tk.END, "链接：" + result.split("\t")[3])
            '''
    
    def uploadWindow(self):
        temp_window = tk.Toplevel()
        temp_window.title("上传文件")
        temp_window.geometry("%dx%d+%d+%d" 
                             %(self.width / 2, self.height / 2, self.width / 4, self.height / 4))
        temp_window.resizable(width=0, height=0)
        
        entry_width = int(self.width / 22)
        tk.Label(temp_window, text='请选择上传文件（csv格式）').grid(row=0,column=0)
        
        #global filename
        filename = tk.StringVar()
        entry_filename = tk.Entry(temp_window, width=entry_width,textvariable=filename)
        entry_filename.grid(row=0,column=1)#输入框
        
        def choose_file():
            temp_window.wm_attributes("-topmost", 0) # 突然置顶
            selectFileName = filedialog.askopenfilename(title='选择文件')  # 选择文件
            filename.set(selectFileName)
            temp_window.wm_attributes("-topmost", 1) # 突然置顶
            #entry_filename.config(tk.DISABLED)
            
        def upload(filename):
            if not filename:
                tk.Label(temp_window, text="请先选择需要上传的文件").grid(row=1,column=0,columnspan=10)
            else:
                name = filename.split("/")[-1]
                tk.Label(temp_window, text=name+"：文件上传中，请稍后...").grid(row=1,column=0,columnspan=10)
                import socket
                import os
                import time
                client = socket.socket()  
                ip_port =(search.HOST, 6666)  # server地址和端口号
                client.connect(ip_port)  
                print("服务器已连接！")
                while True:
                    path=filename
                    filename=os.path.basename(filename)
                    filesize=os.stat(path).st_size
                    #print(filesize)
                    message="post %s %s" % (filename,filesize)
                    message = message.encode()
                    client.send(message)
                    #client.send(filesize)
                    has_sent=0
                    
                    time.sleep(1)
                    
                    with open(path,'rb') as f: 
                        while has_sent!=filesize:
                            data=f.read(1024)
                            client.sendall(data)
                            has_sent+=len(data)
                            process=int(has_sent / filesize * 100)
                            print("\r上传进度：", process)
                    if str(client.recv(4), "utf-8") == "OK":
                        break
                client.close()
                tk.Label(temp_window, text="上传并分析成功！" + filename).grid(row=2,column=0,columnspan=10)
                #self.index = filename.split(".")[0]
                
        submit_button = tk.Button(temp_window, text ="选择文件", command=choose_file)
        submit_button.grid(row=0,column=2)
        submit_button = tk.Button(temp_window, text ="上传", command = lambda:upload(entry_filename.get()))
        submit_button.grid(row=0,column=3)
        
        temp_window.mainloop()
        
    def _convert65535(self, to_convert):
        """Converts a string with out-of-range characters in it into a 
        string with codes in it.
        Based on <https://stackoverflow.com/a/28076205/4865723>.
        This is a workaround because Tkinter (Tcl) doesn't allow unicode
        characters outside of a specific range. This could be emoticons
        for example.
        """
        for character in to_convert[:]:
            if ord(character) > 65535:
                convert_with = '{' + str(ord(character)) + 'ū}'
                to_convert = to_convert.replace(character, convert_with)
        return to_convert
    

if __name__ == "__main__":    
    ui = UI()

