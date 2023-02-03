# Echo-server
import socket

HOST = "127.0.0.1" #Localhost
PORT = 55555 # Порт прослушки должен быть > 1024

# Открываем поток
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
            streamConnect.sendAll(data)
            