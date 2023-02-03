import socket 
from threading import Thread

# IP-адрес и порт нашего сервера
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 55555
# Будем использовать данный разделитель для разделения name & message
separator_token = "<SEP>"

# Инициализируем list/set для всех подключенных клиентких сокетов
client_sockets = set()
# Создадим TCP сокет
s = socket.socket()
# Сделаем порт переиспользуемым
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Привяжем сокет к адресу и порту
s.bind((SERVER_HOST, SERVER_PORT))
# Слушаем ожидаемые подключения
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    Эта функция продолжает прослушивать сообщение из сокета "cs"
    Каждый раз, когда сообщение получено, транслирует его всем другим 
    подключенным клиентам.
    """
    while True:
        try:
            # Продолжаем прослушивать сообщение из сокета "cs"
            msg = cs.recv(1024).decode()
        except Exception as e:
            # Клиент больше не подключен
            # удали его из set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # Если если мы получили сообщение, меняем токен <SEP> 
            # на ":" для хорошего вывода
            msg = msg.replace(separator_token, ": ")
            # Проитерируем все подключенные сокеты
            for client_socket in client_sockets:
                # И отправим сообщение
                client_socket.send(msg.encode())


while True:
    # Продолжаем прослушивать новые подключения все время
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # Добавляем новое подключение клиента в подключенные сокеты
    client_sockets.add(client_socket) 
    # Запускаем новый поток, который прослушивает сообщения каждого 
    # клиента
    t = Thread(target=listen_for_client, args=(client_socket,))
    # СДелаем daemon потока, чтобы он завершался всякий раз, когда 
    # завершается основной поток
    t.daemon = True
    # Запускаем поток
    t.start()
    # Закрываем клиентские сокеты
    for cs in client_sockets:
        cs.close()
    # Закрываем сокет сервера
    s.close()


