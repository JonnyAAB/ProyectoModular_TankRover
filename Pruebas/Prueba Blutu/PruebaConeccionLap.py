import socket

import json

# Definir los datos como un diccionario de Python
datos_a_enviar = {
    "comando": "ENCENDER_LED",
    "parametros": {
        "led": "LED1"
    }
}

# Convertir los datos a una cadena JSON
datos_json = json.dumps(datos_a_enviar)

# Envía la cadena JSON a la Raspberry Pi (por ejemplo, a través de Bluetooth, Wi-Fi o cualquier otro medio de comunicación)


# Configura el cliente
server_host = '192.168.0.44'  # La dirección IP de la Raspberry Pi en la red local
server_port = 12345  # Puerto de escucha (debe coincidir con el puerto del servidor)

# Crea el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

try:
    while True:
        # Envía datos al servidor
        data_to_send = "Hola, Raspberry Pi"
        pd = input("Ingrese posición deseada: ")
        client_socket.send(data_to_send.encode())
        client_socket.send(pd.encode())
except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
