#coding:utf8

import time

from socket import AF_INET,SOCK_STREAM,socket
from thread import start_new
import struct,json
HOST='192.168.1.102'
PORT=11009
BUFSIZE=1024
ADDR=(HOST , PORT)
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)

def sendData(sendstr,commandId):
    """78,37,38,48,9,0"""
    HEAD_0 = chr(78)
    HEAD_1 = chr(37)
    HEAD_2 = chr(38)
    HEAD_3 = chr(48)
    ProtoVersion = chr(9)
    ServerVersion = 0
    sendstr = sendstr
    data = struct.pack('!sssss3I',HEAD_0,HEAD_1,HEAD_2,\
                       HEAD_3,ProtoVersion,ServerVersion,\
                       len(sendstr)+4,commandId)
    senddata = data+sendstr
    return senddata

def resolveRecvdata(data):
    head = struct.unpack('!sssss3I',data[:17])
    lenght = head[6]
    data = data[17:17+lenght]
    return data


def login():
    client.sendall(sendData(json.dumps({"username":"test106","password":"111111"}),101))

def rolelogin():
    client.sendall(sendData(json.dumps({"userId":1915,"characterId":1000001}),103))

def fight():
    client.sendall(sendData(json.dumps({"zjid":1000,"characterId":1000001}),4501))

login()
rolelogin()


def start():
    for i in xrange(100):
        fight()

for i in range(10):
    start_new(start,())
while True:
    pass

