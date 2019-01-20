# 客户端

import socket
import os

BASE_dir=os.path.dirname(os.path.abspath(__file__))
client = socket.socket()  
ip_port =("localhost", 6666)  # server地址和端口号
client.connect(ip_port)  

print("服务器已连接！")

while True:
    content = input(">>>")
    cmd,name = content.split(' ')
    path=os.path.join(BASE_dir,name)
    filename=os.path.basename(path)
    filesize=os.stat(path).st_size
    message='post %s %s'%(filename,filesize)
    client.sendall(bytes(message,'utf-8'))
    has_sent=0
    with open(path,'rb') as f: 
        while has_sent!=filesize:
            data=f.read(1024)
            client.sendall(data)
            has_sent+=len(data)
            print('\r[上传进度]：%s%.2f%%'%('>'*int(has_sent/filesize)*50,
                            (has_sent/filesize)*100),end='')
    print('\n上传成功！%s'%filename)
