import socket
import threading # модуль для многопоточного выполнения кода

def read_socket():
    while True:
        data = client_socket.recv(1024)
        print(data.decode('utf-8'))

HOST = "127.0.0.1"
PORT = 55555

nickname = input("Введите Ваш никнейм")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Задаем сокет ка клиент
client_socket.bind(('', 0)) 
# Уведомляем сервер о подключении
client_socket.sendto((nickname + ' connect to server')
             .encode('utf-8'), (HOST, PORT)) 
client_stream = threading.Thread(target=read_socket)
client_stream.start()

while True:
    message = input("Ваше сообщение: ")
    client_socket(('[' + nickname + ']:' + message).encode('utf-8'), (HOST, PORT))