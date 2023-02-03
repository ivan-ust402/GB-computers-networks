import socket
from threading import Thread
from datetime import datetime

# IP-адрес сервера
# Если сервер не на этой машине, введите частный (сетевой) IP-адрес (например, 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 55555
# мы будем использовать <SEP> для разделения имени клиента и сообщения
separator_token = "<SEP>"

# Инициализируем TCP сокет
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# Подключаемся к серверу
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
# Запрашиваем имя у клиента
name = input("Введите ваше имя: ")

def listen_for_messages():
    """
    Прослушивание сообщений с сервера и вывод их на консоль
    """
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# создаем поток, который прослушивает сообщения для этого клиента и 
# печатает их
t = Thread(target=listen_for_messages)
# сделать поток daemon, чтобы он завершался всякий раз, когда завершается основной поток
t.daemon = True
# Запустить поток
t.start()

# Ожидание сообщений от пользователей с последующей отправкой их на сервер
while True:
    # Вводим сообщение, которое мы хотим отправить на сервер
    to_send = input()
    # Способ выхода из программы
    if to_send.lower() == 'q':
        break
    # Добавим время и имя отправляющего
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"[{date_now}] {name}{separator_token}{to_send}"
    # наконец, отправляем сообщение
    s.send(to_send.encode())
# закрываем сокет
s.close()