import bluetooth

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1  # Puedes usar cualquier número de puerto (1-30)

server_socket.bind(("", port))
server_socket.listen(1)

print("Esperando conexiones Bluetooth...")

client_socket, address = server_socket.accept()
print("Conectado a", address)

while True:
    try:
        data = client_socket.recv(1024)
        if not data:
            break
        print("Datos recibidos:", data.decode())
        # Procesa los datos según tus necesidades
    except Exception as e:
        print("Error:", str(e))
        break

client_socket.close()
server_socket.close()


