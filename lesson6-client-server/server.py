# Echo-server
import socket

HOST = "127.0.0.1" #Localhost
PORT = 55555 # Порт прослушки должен быть > 1024

# Открываем поток
# Константа AF_INET - семейство интернет адресов для IPv4
# SOCK_STREAM - тип сокета для TCP протокола, который будет
# использоваться для передачи сообщений в сети
# .bind() - связываем сокет с кортежем, состоящим из сетевого
# интерфейса и номера порта
# Если вместо определенного HOST передать пустую строку, сервер будет 
# принимать соединения на всех доступных интерфейсах IPv4
# .listen() - позволяет серверу принимать соединения
# .accept() - блокирует выполнение и ожидает входящего соединения. 
# Когда клиент подключается, он возвращает новый объект сокета, 
# в котором содержится новый сокет и кортеж из IP клиента и порта
# клиента. Этот сокет мы используем для связи с клиентом

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
    stream.bind((HOST, PORT))
    stream.listen()
    streamConnect, addrClient = stream.accept()
    with streamConnect:
        print(f'Connected by {addrClient}')
        while True:
            data = streamConnect.recv(1024)
            if not data:
                break
            streamConnect.sendall(data)
