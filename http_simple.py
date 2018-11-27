#!/usr/bin/env python
#coding:utf-8
import socket
import sys
import re
import os
import time
import select
import threading

HEADER_SIZE = 4096

host = '0.0.0.0'
port = 8000

#子进程进行socket 网络请求
def http_socket(client, addr):
    #创建 select 检测 fd 列表
    inputs  = [client]
    outputs = []
    remote_socket = 0
    print("client connent:{0}:{1}".format(addr[0], addr[1]))
    while True:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        try:
            for s in readable:
                if s is client:
                    #读取 http 请求头信息
                    data = s.recv(HEADER_SIZE)
                    if remote_socket is 0:
                        #拆分头信息
                        host_url  = data.split("\r\n")[0].split(" ")
                        method, host_addr, protocol = map(lambda x: x.strip(), host_url)
                        #如果 CONNECT 代理方式
                        if method == "CONNECT":
                            host, port = host_addr.split(":")
                        else:
                            host_addr = data.split("\r\n")[1].split(":")
                            #如果未指定端口则为默认 80
                            if 2 == len(host_addr):
                                host_addr.append("80")
                            name, host, port = map(lambda x: x.strip(), host_addr)
                            #建立 socket tcp 连接
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.connect((host, int(port)))
                        remote_socket = sock
                        inputs.append(sock)
                        if method == "CONNECT":
                            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                            s.sendall("HTTP/1.1 200 Connection Established\r\nFiddlerGateway: Direct\r\nStartTime: {0}\r\nConnection: close\r\n\r\n".format(start_time))
                            continue
                    #发送原始请求头
                    remote_socket.sendall(data)
                else:
                    #接收数据并发送给浏览器
                    resp = s.recv(HEADER_SIZE)
                    if resp:
                        client.sendall(resp)
        except Exception as e:
            print("http socket error {0}".format(e))

#创建socket对象
http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    http_server.bind((host, port))
except Exception as e:
    sys.exit("python proxy bind error {0}".format(e))

print("python proxy start")

http_server.listen(1024)

while True:
    client, addr = http_server.accept()
    http_thread = threading.Thread(target=http_socket, args=(client, addr))
    http_thread.start()
    time.sleep(1)

#关闭所有连接
http_server.close()
print("python proxy close")
