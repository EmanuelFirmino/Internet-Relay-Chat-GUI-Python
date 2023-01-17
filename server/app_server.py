from sys import stdout
import socket
import threading
import json

class IRCServer:
    def __init__(self, address, port):
        self.decoder = 'utf-8'
        self.socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketObj.bind((address, port))
        self.socketObj.listen(20)

        self.clientsThread      = dict()
        self.NICKS           = dict()
        self.CHANNELS           = dict()
        self.CHANNELS['#welcome'] = list()
        self.CHANNELS['#unb']     = list()
        self.DBMessages           = list()
        
        self.listener = threading.Thread(target=self.threadListener)
        self.listener.run()

    def threadListener(self):
        while True:
            try:
                clientSocket, addr = self.socketObj.accept()
                print('Client accepted: ' + str(addr))

            except OSError:
                break

            self.clientsThread[addr] = threading.Thread(target=self.threadService, args=(addr, clientSocket), daemon=True)
            self.clientsThread[addr].run()

    def threadService(self, addr, clientSocket: socket.socket):

        retries = 2
        clientSocket.settimeout(2)

        while True:
            try: 
                message = clientSocket.recv(1024)
            
            except TimeoutError as e:
                print(e)
                clientSocket.close()
                break

            except Exception as e:
                print(e)
                break

            if len(message):
                retries = 2
            else:
                retries -= 1
                if not retries:
                    break
                continue

            decoded_message = json.loads(message.decode(self.decoder))
            response        = json.dumps(self.messageHandler(decoded_message)).encode(self.decoder)
            

            clientSocket.send(response)

    def messageHandler(self, message):
        response = dict()
        command  = message['ACTION']

        # USER --------------------------------------------------------------------

        if   command == 'USER':

            if message['NICKNAME'] in self.NICKS.keys():

                response['STATUS'] = 'ok'
                response['INFO']   = self.NICKS[message['NICKNAME']]
            
            else:
                
                response['STATUS'] = 'fail'

        # -------------------------------------------------------------------------

        elif command == 'PRIVMSG':
            
            response['STATUS'] = 'ok'
            msg = { 'TYPE': message['TYPE'], 'TARGET': message['TARGET'], 'MESSAGE': message['MESSAGE'], 'USER_NICKNAME': message['USER_NICKNAME']}
            self.DBMessages.append(msg)


        elif command == 'REFRESH':
            back = []
            for i in range(message['CURR'], len(self.DBMessages)):
                if message['USER_NICKNAME'] == self.DBMessages[i]['TARGET'] or message['USER_CHANNEL'] == self.DBMessages[i]['TARGET']:
                    back.append(f'{self.DBMessages[i]["MESSAGE"]}')

            if len(back):
                response['STATUS'] = 'ok'
                response['MESSAGES'] = back
                response['CURR'] = len(self.DBMessages)-1
            else:
                response['STATUS'] = 'fail'

        elif command == 'WHO':

            pass

            

        # NICK --------------------------------------------------------------------

        elif command == 'NICK':

            if   message['NICKNAME'] not in self.NICKS.keys(): 
                
                self.NICKS[message['NICKNAME']] = message['USERNAME']
                response['STATUS'] = 'ok'
                
            elif message['USER_NICKNAME'] in self.NICKS.keys():

                del self.NICKS[message['USER_NICKNAME']]
                self.NICKS[message['NICKNAME']] = message['USERNAME']
                response['STATUS'] = 'ok'

            else:

                response['STATUS'] = 'fail'

        # END ---------------------------------------------------------------------

        # JOIN --------------------------------------------------------------------

        elif command == 'JOIN':
            if message['CHANNEL'] in self.CHANNELS.keys() and message['USER_NICKNAME']:

                if self.inAChannel(message['USER_NICKNAME']):
                    self.removeNick(message['USER_NICKNAME'])

                self.CHANNELS[message['CHANNEL']].append(message['USER_NICKNAME'])
                response['STATUS'] = 'ok'

            else:

                response['STATUS'] = 'fail'

        # END ---------------------------------------------------------------------

        # PART --------------------------------------------------------------------

        elif command == 'PART':
            if message['USER_NICKNAME'] and message['USER_CHANNEL']:
                if message['USER_NICKNAME'] in self.CHANNELS[message['USER_CHANNEL']] and message['CHANNEL'] == message['USER_CHANNEL']:
                    self.removeNick(message['USER_NICKNAME'])
                    response['STATUS'] = 'ok'
                else:
                    response['STATUS'] = 'fail'
            else:
                response['STATUS'] = 'fail'

        # END ---------------------------------------------------------------------

        # LIST --------------------------------------------------------------------

        elif command == 'LIST':

            response['CHANNEL_INFO'] = [ [ channel, len(self.CHANNELS[channel]) ] for channel in self.CHANNELS.keys() ]
            response['STATUS']       = 'ok'

        # END ---------------------------------------------------------------------

        elif command == 'REFRESH':
            msgs = []
            for msg in self.DBMessages:
                if message['USER_NICKNAME'] == msg['TARGET'] or message['USER_CHANNEL'] == msg['TARGET']:
                    msgs.append(f'{message["USERNAME"]}: {msg["MESSAGE"]}')
            
            if len(msgs):
                response['STATUS'] = 'ok'

            else:
                response['STATUS'] = 'fail'

        elif command == 'QUIT':
            response['STATUS'] = 'QUIT'

        # ERR ---------------------------------------------------------------------

        else:
            response['STATUS'] = 'ERR UNKNOWNCOMMAND'

        # END ---------------------------------------------------------------------
        
        return response 
    
    def inAChannel(self, nick) -> bool:
        for channel in self.CHANNELS.keys():
            if nick in self.CHANNELS[channel]:
                return True
        return False

    def removeNick(self, nick):
        for channel in self.CHANNELS.keys():
            for index in range(len(self.CHANNELS[channel])):
                if nick == self.CHANNELS[channel][index]:
                    del self.CHANNELS[channel][index]



if __name__ == '__main__':
    IRCServer('127.0.0.1', 1900)