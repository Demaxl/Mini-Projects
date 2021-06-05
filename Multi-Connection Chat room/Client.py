import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_name = 'localhost'
HOST = socket.gethostbyname(server_name)
PORT = 5050
DISCONNECT_MESSAGE = '!DISCONNECT'
disconnected = False


def handle_send_msg(username):
    global disconnected
    
    client.send(username.encode())
    join_msg = client.recv(1024).decode()
    print(join_msg)
    
    connected = True
    receive = threading.Thread(target=handle_recv_msg)
    receive.start()

    while connected:
        msg = input('You:\n')
        if msg == DISCONNECT_MESSAGE:
            client.send(DISCONNECT_MESSAGE.encode())
            disconnected = True
            leave_msg = client.recv(1024).decode()
            print(leave_msg)
            client.close()
            break
        else:
            client.send(msg.encode())
    
    
def handle_recv_msg():
    while True and not disconnected:
        incoming = client.recv(8192).decode()
        if len(incoming) > 0:
            name = incoming.split(':\n')[0]
            if name.lower() == username.lower():
                print()
            else:
                print(incoming)
                print()


if __name__ == '__main__':
    client.connect((HOST, PORT))
    username = input('Server is asking for your name:\n')
    handle_send_msg(username)
                    


