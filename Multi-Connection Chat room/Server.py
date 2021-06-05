import socket
import threading


HOST = ''
PORT = 5050
DISCONNECT_MESSAGE = '!DISCONNECT'


class Server:
    connections = 0
    
    def __init__(self, server):
        self.server = server
        self.client_data = {}
        self.started_receiving = False
        
    
    def handle_client(self, client, addr):
        try:
            Server.connections += 1
            
            username = client.recv(1024).decode()
            print(f'[NEW CONNECTION] Got a connection from {addr}\nUsername: {username}\n')
            client.send(f'You have joined the chat.\nTo leave send "{DISCONNECT_MESSAGE}"\n'.encode())
            try:
                for c in self.client_data.keys():
                    c.send(f'{username} has joined the chat\n'.encode())
            except (RuntimeError, KeyError):
                pass
            self.client_data[client] = [username, '']
            
            if Server.connections > 1 and not self.started_receiving:
                self.started_receiving = True
                print('[STARTED] A chat has started\n')
                handle = threading.Thread(target=self.handling_messages)
                handle.start()
            
            while True:
                msg = client.recv(1024).decode()
                if msg == DISCONNECT_MESSAGE:
                    client.send('You left the chat'.encode())
                    del self.client_data[client]
                    client.close()
                    
                    print(f'[INFO] {username} has left\n')
                    try:
                        for c in self.client_data.keys():
                            c.send(f'{username} has left\n'.encode())
                    except (RuntimeError, KeyError):
                        pass
                    Server.connections -= 1
                    if Server.connections < 2:
                        self.started_receiving = False
                    break
                self.client_data[client][1] = msg
        except ConnectionResetError:
            pass
    
    def handling_messages(self):
        while True:
            messages = []
            try:
                for client, info in self.client_data.items():
                    if len(info[1]) > 0:
                        messages.append(f'{info[0]}:\n{info[1]}\n')
                    self.client_data[client][1] = ''
                    
                for client in self.client_data.keys():
                    for msg in messages:
                        client.send(msg.encode())
            except (RuntimeError, KeyError):
                pass
                
                
    def start(self):
        self.server.listen()
        while True:
            client, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, addr))
            thread.start()
            


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    
    s = Server(server)
    print('[STARTING] Server is running...')
    s.start()
    


