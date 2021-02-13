import socket

con = socket.create_connection(('127.0.0.1', 8888))
com = '\n'

con.sendall(com.encode())
data = con.recv(2048).decode(('utf-8'))
con.close()

print(ascii(data))