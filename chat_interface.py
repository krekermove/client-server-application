import customtkinter as CTk
import tkinter
import threading
from client import Client


class Window_chat(CTk.CTk):
    def __init__(self):
        #create window
        super().__init__()
        self.geometry('{}x{}'.format(int(self.winfo_screenwidth()*0.9), int(self.winfo_screenheight()*0.6)))
        self.title("КЛИЕНТО-СЕРВЕРНОЕ ПРИЛОЖЕНИЕ С ФУНКЦИЕЙ ВЫВОДА ПОГОДЫ")
        self.resizable(True, True)
        self.grid_rowconfigure(0)
        self.columnconfigure(0)
        self._set_appearance_mode("dark")

        self.client = None
        self.chat_frame = None

        #add label for important message
        self.info = CTk.CTkLabel(self, text = 'Нажмите подключится к серверу. \n Введите хост и порт, если хотите сменить сервер.')
        self.info.grid(row=0, column=1)

        #add label for important message
        self.label = CTk.CTkLabel(self, text = 'Подключение')
        self.label.grid(row=1, column=1)

        #add entry for text message
        self.entry = CTk.CTkEntry(self, placeholder_text="Введите имя")
        self.entry.grid(row=3, column=0, padx=20, pady=20)

        #create menu
        self.screen_of_input_name()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    #close window
    def on_closing(self):
        print("Выводится при попытке закрытия окна")
        #проверка на существование объектов
        try:
            if self.chat_frame is not None:
                self.chat_frame.destroy()
            if self.client is not None:
                self.client.__del__()
        except:
            print('Сервер выдал ошибку')
        finally:
            self.destroy()  # Закрыть окно

    # scree with start input name
    def screen_of_input_name(self):
        def button_command():
            #проверка ввода имени and start server
            _name = self.entry.get()
            if ' ' in _name or _name == '':
                self.label.configure(text = "Имя не подходит")
            else:
                self.run_speak_with_server(_name, host.get(), port.get())
                button.destroy()
                host.destroy()
                port.destroy()

        button = CTk.CTkButton(self, text = 'Подключиться', command = button_command)
        button.grid(row=3, column=1, padx=20, pady=20)

        host = CTk.CTkEntry(self, placeholder_text="Host")
        host.grid(row=0, column=0, padx=20, pady=20)

        port = CTk.CTkEntry(self, placeholder_text="Port")
        port.grid(row=1, column=0, padx=20, pady=20)

    # start work client server
    def run_speak_with_server(self, name, host, port):
        self.label.configure(text = "CHAT")

        #client
        try:
            if host == '' or port == '':
                self.client = Client(name)
            else:
                self.client = Client(name, host, int(port))
            conn = self.client.connect()
            if conn:
                self.label.configure(text = "Успешное подключение")
                self.info.configure(text = 'Пишите сообщения\n /info - вывести кол-во сообщений и пользователей \n /pogoda - команда, которая выводит погоду в городе Санкт-Петебург \n на текущий момент времени')
            else:
                self.label.configure(text = "Это имя уже занято!")
                self.screen_of_input_name()
                return
        except Exception as e:
            print(e)
            self.label.configure(text = "Ошибка подключения")
            self.screen_of_input_name()
            return

        #add button for send message
        def button_command():
            if self.button.cget('text') == 'Выход':
                self.on_closing()
            else:

                self.client.new_message('message', self.entry.get())
        self.button = CTk.CTkButton(self, text = 'Send', command = button_command, fg_color="red")
        self.button.grid(row=3, column=2, padx=20, pady=20)

        # add scroll char
        self.chat_frame = Chat_frame(master=self, client = self.client, label = self.label, button = self.button, width=600, height=250)
        self.chat_frame.grid(row=0, column=0)

class Chat_frame(CTk.CTkScrollableFrame):
    def __init__(self, master, client, label, button, **kwargs):
        super().__init__(master, **kwargs)
        self.button = button
        self.label = label
        self.client = client

        #thread for chat print
        t = threading.Thread(target=self.print_message, daemon=True)
        t.start()

    def print_message(self):
        message = []
        lenght_chat = 100
        quit = False
        i = 1
        while not quit:
            try:
                # recive message
                quit, _text = self.client.listen()
                if quit:
                    self.label.configure(text = _text)
                    break
                #pozition in chat frame
                _len = len(message)
                message.append(CTk.CTkLabel(self, text = _text))
                message[_len].grid(row=i, column=0, padx=20)
                if(_len == lenght_chat):
                    message.pop(0).destroy()
                i+=1
            except Exception as e:
                self.label.configure(text = 'Подключение разорвано')
                self.button.configure(text = "Выход")
                print('Работа закончена!', e)
                break
        self.label.configure(text = 'Подключение разорвано')
        self.button.configure(text = "Выход")

if __name__ == '__main__':
    app = Window_chat()
    app.mainloop()
