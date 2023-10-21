import socket
from time import sleep,time
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
server_port = 12346  # Puerto de escucha (debe coincidir con el puerto del servidor)

# Crea el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

try:
    while True:
        # Definir los datos a enviar en formato JSON
        datos_a_enviar = {
            "comando": "ENCENDER_LED",
            "parametros": {
                "pd": 32,
                "kp": 0.4,
                "kd": 0.1
            }
        }

        # Convertir los datos a una cadena JSON
        datos_json = json.dumps(datos_a_enviar)

        # Enviar los datos al servidor (Raspberry Pi)
        client_socket.send(datos_json.encode())
        sleep(1)


except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
