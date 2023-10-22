import socket
import json

# Configura el cliente
server_host = '192.168.0.44'  # La dirección IP de la Raspberry Pi en la red local
server_port = 1342  # Puerto de escucha (debe coincidir con el puerto del servidor)

# Crea el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# Recibir los datos del servidor
received_data = client_socket.recv(1024).decode()

# Convertir los datos JSON a una lista
data_list = json.loads(received_data)

# Imprimir la lista recibida
print("Lista recibida:", data_list)

# Cerrar la conexión
client_socket.close()
