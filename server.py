import socket
from _thread import *
import sys

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'hostIPV4' # Replace 'hostIPV4' with the ipv4 address of the computer you are using as a server
port = 65432

server_ip = socket.gethostbyname(server)

try:
    server_socket.bind((server, port))

except socket.error as e:
    print(str(e))

server_socket.listen(2)
print("Waiting for a connection")

currentId = "0"

screen_width = 500
screen_height = 500
pos = ["0:"+ str(screen_width - 20) + str(screen_height/2 - 70), "1:"+ str(10) + str(screen_height/2 - 70)]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print("Sending: " + reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = server_socket.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))
