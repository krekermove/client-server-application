import datetime
import socket
from threading import Thread

class Client():
    def __init__(self, name='user', host='localhost', port=5555):
        self.name = f'[{name}]'
        self.server = (host, port)

    def connect(self):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect(self.server)

        self.new_message('connect')

        # check name
        data = self.client_sock.recv(1024).decode('utf-8')  # [state] text
        _data = data.split()
        if _data[0] == '[ERR]':
            return False
        return True

    def new_message(self, state, text=''):
        event_massage = {'connect': '[CON]',
                         'disconnect': '[DIS]',
                         'message': '[MES]',
                         'command': '[COM]'
                         }

        if text != '' and text[0] == '/':
            state = 'command'
        _text = event_massage[state] + ' ' + self.name + ' ' + text
        self.client_sock.sendall(bytes(_text, "utf8"))

    def disconnect(self):
        self.new_message('disconnect')
        self.client_sock.close()
        print('Connection is clossed')

    def __del__(self):
        self.disconnect()

    def listen(self) -> (bool, str):
        try:
            print('wait')
            data = self.client_sock.recv(1024).decode('utf-8')  # [state] text
            _data = data.split()
            if _data[1]==self.name:
                _data[1]='[Вы]'

            return False, ' '.join(_data[1:])
            # if _data[0]=='[MES]':
            #     print('1')
            #     return False, ' '.join(_data[1:])
            # elif _data[0]=='[ERR]':
            #     print('2')
            #     return True, ' '.join(_data[1:])
        except:
            return True, 'help'