# echo-client
import socket

HOST = "127.0.0.1" #Имя домена или IP адрес сервера
PORT = 55555 # Порт, который использует сервер
# Создаем поток
# .connect() - подключаемся к серверу
# .sendall() - отправляем сообщение серверу
# .recv() - чистаем ответ сервера
# print(data) - распечатываем ответ сервера 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientStream:
    clientStream.connect((HOST, PORT))
    clientStream.sendall(b'Hello world')
    data = clientStream.recv(1024)

print(f"Received {data!r}")