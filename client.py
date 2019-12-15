# coding=utf-8
import socket


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

while 1:
    msg = raw_input('input your message:')
    client.send(msg)
    data = client.recv(1024)
    print 'Received message: [%s]' % data
