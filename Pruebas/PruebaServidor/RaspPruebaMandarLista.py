import socket
import json

# Configura el servidor
# ----------------------------------------------------------------------
server_host = '192.168.0.44'  # Escucha en todas las interfaces de red
server_port = 1342  # Puerto de escucha (puedes usar cualquier número de puerto)
print(f"Esperando conexiones en {server_host}:{server_port}")

# Crea el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)  # Acepta una sola conexión entrante

# Acepta una conexión entrante
client_socket, client_address = server_socket.accept()
print(f"Conectado a {client_address}")
# ----------------------------------------------------------------------

# Lista que deseas enviar al cliente
data_to_send = [1, 2, 3, 4, 5]

# Convertir la lista a JSON
data_json = json.dumps(data_to_send)

# Enviar los datos al cliente
client_socket.send(data_json.encode())

# Cerrar la conexión
client_socket.close()
server_socket.close()
