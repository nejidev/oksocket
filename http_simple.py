#!/usr/bin/env python
#coding:utf-8
import socket
import sys
import re
import os
import time
import urllib
import urllib2
import threading

HEADER_SIZE = 4096

host = '0.0.0.0'
port = 8000

#子进程进行socket 网络请求
def http_socket(conn, addr):
    print("client connent:{0}:{1}".format(addr[0], addr[1]))
    try:
        #读取 http 请求头信息
        request_header = conn.recv(HEADER_SIZE)
        #拆分头信息
        host_addr = request_header.split("\r\n")[1].split(":")
        #如果未指定端口则为默认 80
        if 2 == len(host_addr):
            host_addr.append("80")
        name, host, port = map(lambda x: x.strip(), host_addr)
        #建立 socket tcp 连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))
        #发送原始请求头
        sock.sendall(request_header)
        #接收数据并发送给浏览器
        while(True):
            resp = sock.recv(1024)
            if resp:
                conn.send(resp)
            else:
                break
        #关闭连接   
        sock.close()
    except Exception as e:
        print("http socket error")
        print(e)

#创建socket对象
http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    http_server.bind((host, port))
except:
    sys.exit("python proxy bind error ")

print("python proxy start")

http_server.listen(1024)

while True:
    conn, addr = http_server.accept()
    http_thread = threading.Thread(target=http_socket, args=(conn, addr))
    http_thread.start()
    time.sleep(1)

#关闭所有连接
http_server.close()
print("python proxy close")
