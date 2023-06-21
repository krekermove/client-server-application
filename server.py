import time
import socket
import base64
import threading
import pyowm
import datetime


class Server():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.all_client = []
        self.client_counter = 0
        self.message_counter = 0

        # Запускаем прослушивание соединений
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(0)
        threading.Thread(target=self.connect_handler).start()
        print('Сервер запущен!')

    # Обрабатываем входящие соединения
    def connect_handler(self):
        while True:
            client, address = self.server.accept()
            if client not in self.all_client:
                self.all_client.append(client)
                self.client_counter += 1
                threading.Thread(target=self.message_handler, args=(client,)).start()
                client.send('Успешное подключение к чату!'.encode('utf-8'))
            time.sleep(1)

    # Обрабатываем отправленный текст
    def message_handler(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                print(message)
                self.message_counter += 1
                current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                _message = message.split()
                message = ' '.join(_message[1:])
                if _message[0] == '[COM]':
                    if _message[2] == '/info':
                        self.message_counter -= 1
                        message = 'Кол-во пользователей: ' + str(self.client_counter) + '\n' + 'Кол-во сообщений: ' + str(self.message_counter)
                    if _message[2] == '/pogoda':
                        message = 'Погода в городе Санкт-Петербург: ' + self.pogoda()
                elif _message[0] == '[CON]':
                    message += ' успешно подключился к серверу!'
                elif _message[0] == '[DIS]':
                    message = f"[MES] [{current_datetime}] {_message[1]} отключился от сервера"
                    print(message)
                    client_socket.close()
                    self.all_client.remove(client_socket)
                    self.client_counter-=1
                    for client in self.all_client:
                        client.send(message.encode('utf-8'))
                    break
                message = "ds [" + str(current_datetime) + "] " + message
                for client in self.all_client:
                    client.send(message.encode('utf-8'))
                time.sleep(1)
            except:
                print("Problems client part1")
                break

    def pogoda(self)->str:
        word = 'Санкт-Петербург'
        owm = pyowm.OWM('7aa4a1de7c9552e9eaf8d99f074b9c46')

        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(word)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        return str(temperature)

if __name__ == '__main__':
    myserver = Server('localhost', 5555)