import socket
import threading  # threading 모듈 사용
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(10)
print("Waiting for a connection")

currentId = "0"
pos = [f'{i}:0,0' for i in range(10)] # dataset


threading.Lock()
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = str(int(currentId)+1)

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            print("Received: " + reply)
            
            arr = reply.split(":")
            id = int(arr[0])
            pos[id] = reply

            send = ('|').join(pos)
            print("Sending: " + send)

            conn.sendall(str.encode(send))
        except Exception as e:
            print(e)
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    # threading 모듈을 사용해 새로운 스레드 생성
    client_thread = threading.Thread(target=threaded_client, args=(conn,))
    client_thread.start()
