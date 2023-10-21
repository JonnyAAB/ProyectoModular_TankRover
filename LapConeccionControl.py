import socket
from time import sleep,time
import json
import msvcrt
import os

# IMPORTANTE #
#Hasta ahora no he podido ver como eliminar las graficas asi que se necesita realizar un comentario con el comando nano
# cd ProyectoModular
# nano ConnecionConControlRasp.py
# Comentar la funcion al final del while con un # y guardarlo con ctr+O y enter
# Por ultimo correr el programa 
# sudo python3 ConnecionConControlRasp.py

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
server_port = 1341  # Puerto de escucha (debe coincidir con el puerto del servidor)

# Crea el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))
i=0
try:
    while True:
        # Definir los datos a enviar en formato JSON
        pd = int(input("Ingrese posición deseada: "))
        kp = float(input("Ingrese kp: "))
        kd = float(input("Ingrese kd: "))
        t = int(input("Ingrese tiempo simulación: "))
        if i>=1:
            rein = int(input("Quiere reiniciar la posición (1:si, 0:no): "))
            if rein>=1:
                rein = True
            else:
                rein = False
        else:
            rein = False
        datos_a_enviar = {
            "comando": "PropiedadesControl",
            "parametros": {
                "pd": pd,
                "kp": kp,
                "kd": kd,
                "t" : t,
                "rein":rein
            }
        }

        # Convertir los datos a una cadena JSON
        datos_json = json.dumps(datos_a_enviar)

        # Enviar los datos al servidor (Raspberry Pi)
        client_socket.send(datos_json.encode())

        print("Presiona una tecla para continuar o esc (escape) para salir")
        tecla = msvcrt.getch()  # Espera hasta que se presione una tecla
        if tecla == b'\x1b':  # Verifica si se presionó la tecla "Esc" (valor ASCII '\x1b')
            print("Saliendo del programa.")
            client_socket.close()
            break
        else:
            print("Continuando después de presionar una tecla.")
        i=i+1
        os.system('cls')


except KeyboardInterrupt:
    pass

finally:
    client_socket.close()
