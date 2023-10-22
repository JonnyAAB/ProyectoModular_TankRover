import socket
import json

# Crear un socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))  # Enlazar a una dirección y puerto
server_socket.listen(1)  # Escuchar una conexión

print("Esperando una conexión...")
client_socket, client_address = server_socket.accept()

# Lista que deseas enviar al cliente
data_to_send = [1, 2, 3, 4, 5]

# Convertir la lista a JSON
data_json = json.dumps(data_to_send)

# Enviar los datos al cliente
client_socket.send(data_json.encode())

# Cerrar la conexión
client_socket.close()
server_socket.close()
