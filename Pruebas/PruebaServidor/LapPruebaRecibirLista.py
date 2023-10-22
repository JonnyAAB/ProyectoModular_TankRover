import socket
import json

# Crear un socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("IP_DEL_SERVIDOR", 12345))  # Reemplaza "IP_DEL_SERVIDOR" por la dirección IP del servidor

# Recibir los datos del servidor
received_data = client_socket.recv(1024).decode()

# Convertir los datos JSON a una lista
data_list = json.loads(received_data)

# Imprimir la lista recibida
print("Lista recibida:", data_list)

# Cerrar la conexión
client_socket.close()
