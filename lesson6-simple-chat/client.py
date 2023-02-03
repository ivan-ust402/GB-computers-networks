import socket
import threading # модуль для многопоточного выполнения кода


def read_message():
    while True:
        data = client_socket.recv(1024)
        print(data.decode('utf-8'))

def send_message():
    while True:
        message = input()
        client_socket.sendto(('[' + nickname + ']: ' + message).encode('utf-8'), server)

server = "127.0.0.1", 55555

nickname = input("Введите Ваш никнейм: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Задаем сокет ка клиент
client_socket.connect((server)) 
# Уведомляем сервер о подключении
client_socket.sendto((nickname + ' connected to server')
             .encode('utf-8'), server) 
get_thread = threading.Thread(target=read_message)
send_thread = threading.Thread(target=send_message)
get_thread.start()
send_thread.start()
