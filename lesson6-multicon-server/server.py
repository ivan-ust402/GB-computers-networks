# multiconnection server
# import sys
import socket
import selectors
import types


sel = selectors.DefaultSelector()

# HOST, PORT = sys.argv[1], int(sys.argv[2])
HOST = "127.0.0.1"
PORT = 55555

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listening_socket.bind((HOST, PORT))
listening_socket.listen()
print(f"Listening on {(HOST, PORT)}")
# Вызовы, сделанные на этот сокет, больше не будут блокироваться.
listening_socket.setblocking(False) 
# sel.register()регистрирует сокет для отслеживания
sel.register(listening_socket, selectors.EVENT_READ, data=None)


def accept_wrapper(sock):
    conn, addr = sock.accept() # Должен быть готов к чтению
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) # Должен быть готов к чтению
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb) # Should be ready to write
            data.outb = data.outb[sent:]

try:
    while True:
        # sel.select(timeout=None) блокируется до тех пор, пока не 
        # появятся сокеты, готовые к вводу-выводу.
        # Он возвращает список кортежей, по одному для каждого сокета. 
        # Каждый кортеж содержит key и mask.
        # key - ключ именнованного кортежа, который содержит маску событий готовых операций
        # Если key.data == None, то мы знаем, что это от прослушивающего 
        # сокета и нам нужно принять соединение
        # Вызываем собственную функцию accept_wrapper(), чтобы получить
        # новый объект сокета и зарегистрировать его в селекторе
        # Если key.data не None, то мы знаем, что это клиентский сокет, который уже был принят, и нам его нужно обслужить
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()

