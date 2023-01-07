from db_users import Database
from time     import sleep
from queue    import Queue
import socketserver
import threading

global netData

class queueThread(Queue):

    def insert(self, data):
        self.put(data)

    def catch(self):
        return self.get()

    def has_requisition(self):
        return self.qsize() > 0

class ircServer(socketserver.BaseRequestHandler):

    def handle(self):

        while ( True ):

            self.data = self.receive()
            self.action = self.data.split()
            print(self.data)

            if 1:
    
                if  self.action[0]  == 'USER':
                    print('ok')
                    self.send('Tudo funcionando!')
                elif self.action == 'NICK':
                    print('NICK COMMAND!')
                elif self.action == 'JOIN':
                    print('JOIN COMMAND!')
                elif self.action == 'PART':
                    print('PART COMMAND!')
                elif self.action == 'LIST':
                    print('LIST COMMAND!')
                elif self.action == 'PRIVMSG':
                    print('PRIVMSG COMMAND!')
                elif self.action == 'WHO':
                    print('WHO COMMAND!')
                elif self.action == 'QUIT':
                    print('this is QUIT!')                    
                else:
                    print('ERR UNKNOWNCOMMAND')
                break

    def receive(self):
        self.encode       = 'utf-8'
        self.bytes_length = 4096
        return self.request.recv(self.bytes_length).decode(self.encode)

    def send(self, message) -> None:
        self.encode       = 'utf-8'
        self.request.sendall(message.encode(self.encode))

class ircThreaded(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == '__main__':

    netData = queueThread()
    host = '0.0.0.0'
    port = 1900

    sock    = ircServer
    server  = ircThreaded((host, port), sock)
    server.allow_reuse_address = True

    sThreaded = threading.Thread(target=server.serve_forever)
    sThreaded.daemon = True
    sThreaded.start()

    print(f'[+] Server iniciado em {host}:{port} [+] ')

    while ( True ):
           sleep(10)
           