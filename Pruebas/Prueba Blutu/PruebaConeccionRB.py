import socket

# Configura el servidor
server_host = '0.0.0.0'  # Escucha en todas las interfaces de red
server_port = 12345  # Puerto de escucha (puedes usar cualquier número de puerto)

# Crea el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)  # Acepta una sola conexión entrante

print(f"Esperando conexiones en {server_host}:{server_port}")

# Acepta una conexión entrante
client_socket, client_address = server_socket.accept()
print(f"Conectado a {client_address}")

# Lee y procesa los datos recibidos
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    print("Datos recibidos:", data.decode())
    # Procesa los datos según tus necesidades

client_socket.close()
server_socket.close()

