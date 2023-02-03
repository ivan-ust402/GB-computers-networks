import socket
import threading # модуль для многопоточного выполнения кода

def read_socket():
    while True:
        data = client_socket.recv(1024)
        print(data.decode('utf-8'))

server = "127.0.0.1", 55555

nickname = input("Введите Ваш никнейм: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Задаем сокет ка клиент
client_socket.bind(('', 0)) 
# Уведомляем сервер о подключении
client_socket.sendto((nickname + ' connect to server')
             .encode('utf-8'), server) 
client_stream = threading.Thread(target=read_socket)
client_stream.start()

while True:
    message = input()
    client_socket.sendto(('[' + nickname + ']:' + message).encode('utf-8'), server)