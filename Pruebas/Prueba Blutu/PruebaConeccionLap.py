import socket

# Configura el cliente
server_host = 'Dirección IP de la Raspberry Pi'  # La dirección IP de la Raspberry Pi en la red local
server_port = 12345  # Puerto de escucha (debe coincidir con el puerto del servidor)

# Crea el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

# Envía datos al servidor
data_to_send = "Hola, Raspberry Pi"
client_socket.send(data_to_send.encode())

client_socket.close()
