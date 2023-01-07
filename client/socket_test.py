import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 1900))

while ( True ):
    s.sendall(input().encode('utf-8'))
    print(s.recv(4096).decode('utf-8'))