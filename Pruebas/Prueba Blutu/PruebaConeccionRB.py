import socket
import json

# Configura el servidor
server_host = '192.168.0.44'  # Escucha en todas las interfaces de red
server_port = 12346  # Puerto de escucha (puedes usar cualquier número de puerto)

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
        # Recibir los datos enviados
        data = client_socket.recv(1024).decode()
        
        # Cargar los datos recibidos en estructura Python de Json
        datos = json.loads(data)

        # Procesar los datos según el tipo de comando
        comando = datos["comando"]
        parametros = datos.get("parametros", {})

        if comando == "Propiedades del Controo":
            pd = parametros["pd"]
            kp = parametros["kp"]
            kd = parametros["kd"]
            tiempo = parametros["tiempo"]
            
            # Realiza la acción correspondiente, como encender el LED
            print("Asi se mandan datos ", pd, " ", kp, " ", kd, "Suma: ", pd+kp+kd)
        
        # Procesa los datos según tus necesidades
except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
    server_socket.close()

