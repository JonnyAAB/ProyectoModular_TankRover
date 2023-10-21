import socket
import json




# Configura el servidor
server_host = '192.168.0.44'  # Escucha en todas las interfaces de red
server_port = 12345  # Puerto de escucha (puedes usar cualquier número de puerto)

# Crea el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(1)  # Acepta una sola conexión entrante

print(f"Esperando conexiones en {server_host}:{server_port}")

# Acepta una conexión entrante
client_socket, client_address = server_socket.accept()
print(f"Conectado a {client_address}")

try:
    # Lee y procesa los datos recibidos
    while True:
        data = client_socket.recv(1024)
        # ~ if not data:
            # ~ break
        texto = data.decode()
        print(texto)
        # ~ print("Datos recibidos:", data.decode())
        # Recibir la cadena JSON (por ejemplo, a través de sockets, Bluetooth, etc.)
        datos_recibidos = "..."  # Aquí deberías asignar la cadena recibida

        # Convertir la cadena JSON a una estructura de datos de Python
        datos = json.loads(datos_recibidos)

        # Procesar los datos según el tipo de comando
        comando = datos["comando"]
        parametros = datos["parametros"]

        if comando == "ENCENDER_LED":
            led = parametros["led"]
            print("Asi se mandan datos")
            # Realiza la acción correspondiente, como encender el LED
        
        # Procesa los datos según tus necesidades
except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
    server_socket.close()

