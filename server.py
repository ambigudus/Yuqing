# 服务器端

import socket
import os
from process import Process

def receivefile():
    BASE_dir=os.path.dirname(os.path.abspath(__file__))
    server = socket.socket()
    IP_port=('0.0.0.0',6666) #clientIP及端口
    server.bind(IP_port) 
    server.listen(3)  

    print("监听开始..\n等待连接......")

    while True:
        conn, addr = server.accept()  
        print("已连接！ conn:", conn, " addr:", addr[0],':',addr[1])  

        while True:
            data = conn.recv(1024).decode()
            if not data: 
                print("客户端断开连接")
                break
            
            cmd, filename, filesize=data.split(' ')
            filesize=int(filesize)
            
            if cmd =="post":
                path=os.path.join(BASE_dir,'data',filename)
                has_received=0
            with open(path,'wb') as f: 
                while has_received!=filesize:
                    size = 0  # 准确接收数据大小，解决粘包
                    if filesize - has_received > 1024: 
                        size = 1024
                    else:  
                        size = filesize - has_received

                    data = conn.recv(size)  
                    f.write(data)
                    has_received += len(data)
                    print('\r[保存进度]:%s%.2f%%'%('>'*int(has_received/filesize)*50,
                            (has_received/filesize)*100),end='')
            print('\n%s 保存成功！'%filename)
            path = path.replace("\\","/")
            
            Process(path,filename.split('.')[0]) #处理数据
            conn.send(bytes("OK",'utf-8'))
            #server.close()
                
    

if __name__=='__main__':
    receivefile()
    

