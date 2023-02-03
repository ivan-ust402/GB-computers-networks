import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Датаграммный сокет — это сокет, предназначенный для передачи данных в 
# виде отдельных сообщений (датаграмм). По сравнению с потоковым сокетом, 
# обмен данными происходит быстрее, но является ненадёжным: сообщения 
# могут теряться в пути, дублироваться и переупорядочиваться. 
# Датаграммный сокет допускает передачу сообщения нескольким получателям 
# (multicasting) и широковещательную передачу (broadcasting).

HOST = "127.0.0.1"
PORT = 55555

sock.bind((HOST, PORT))
clients = []
print(f"Start server {HOST}:{PORT}")

while True:
    data, address = sock.recvfrom(1024) 
    print(address[0], address[1])
    if address not in clients:
        clients.append(address)
    for client in clients:
        if client == address:
            continue # Не отправлять данные клиенту, который их прислал
        sock.sendto(data, client)

