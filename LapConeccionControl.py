import socket
from time import sleep,time
import json
import msvcrt
import os
import matplotlib.pyplot as plt
import keyboard

# IMPORTANTE #
# Hasta ahora no he podido ver como eliminar las graficas asi que se necesita realizar un comentario con el comando nano (Ya no importa esta wea, imprimo aqui xD)
# cd ProyectoModular
# nano ConnecionConControlRasp.py
# Comentar la funcion al final del while con un # y guardarlo con ctr+O y enter
# Por ultimo correr el programa 
# sudo python3 RaspConeccionControl.py

def muestraGraficas(tiempo,pos,pdPlot,control,control1,control2,errorPlot):
    #Zona de Graficas
    plt.figure(1)
    plt.plot(tiempo,pos,label='Posición Actual', color='blue',linestyle = '-')
    plt.plot(tiempo,pdPlot,label='Posición Deseada', color='red',linestyle='--')
    # ~ plt.ylim(-100,100)
    # ~ plt.axis([xmin,xmax,ymin,ymax])
    plt.title("Grafica Posición")
    plt.xlabel("Tiempo")
    plt.ylabel("Posición")
    plt.legend()
    plt.grid(True)

    plt.figure(2)
    plt.plot(tiempo,control, label='Accion de Control', color='blue',linestyle = '-')
    plt.plot(tiempo,control1, label='Accion de Control Motor 1', color='red',linestyle = '-')
    plt.plot(tiempo,control2, label='Accion de Control Motor 2', color='green',linestyle = '-')
    plt.title("Grafica Accion de Control")
    plt.xlabel("Tiempo")
    plt.ylabel("Acción de Control")
    plt.legend()
    plt.grid(True)
	
    plt.figure(3)
    plt.plot(tiempo,errorPlot, label= 'Error', color='blue',linestyle = '-')
    plt.title("Grafica Error")
    plt.xlabel("Tiempo")
    plt.ylabel("Error")
    plt.grid(True)
    plt.legend()

	#Muestra las graficas
    plt.show()
	
	#	sleep(1)
    plt.close("all")
# # -----------------------------------------------------------------------

# Configura el cliente
server_host = '192.168.137.37'  # La dirección IP de la Raspberry Pi en la red local
server_port = 1341  # Puerto de escucha (debe coincidir con el puerto del servidor),
                    # puede ser cualqier puerto solo tienen que coincidir y que no se este utilizando

# Crea el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

i=False  # Operador auxiliar para reinicio de posición
os.system('cls')    # Limpias la consola

try:
    while True:
        # Definir los datos a enviar en formato JSON
        pd = int(input("Ingrese posición deseada: "))
        kp = float(input("Ingrese kp: "))
        kd = float(input("Ingrese kd: "))
        t = int(input("Ingrese tiempo simulación: "))
        if i:
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
        
        # Datos recibidos
        # -------------------------------------------------------------------------
        # Recibir los datos del servidor
        # Recibir la longitud de los datos
        data_length = int(client_socket.recv(1024).decode())

        # Enviar confirmación al servidor (opcional)
        client_socket.send("OK".encode())

        # Recibir los datos en fragmentos
        received_data = ''
        received = 0

        while received < data_length:
            chunk = client_socket.recv(1024).decode()
            received_data += chunk
            received += len(chunk)

        # Desempaquetar los datos
        data_received = json.loads(received_data)

        # Acceder a los datos
        comando = data_received["comando"]
        parametros = data_received["parametros"]
        
        # Obteniendo datos de las listas
        if comando == "Graficas":
            tiempo = parametros["tiempo"]
            pos = parametros["pos"]
            pdPlot = parametros["pdPlot"]
            control = parametros["control"]
            control1 = parametros["control1"]
            control2 = parametros["control2"]
            errorPlot = parametros["errorPlot"]
        # -------------------------------------------------------------------------

        # Mandamos a llamar a la función de graficas
        muestraGraficas(tiempo,pos,pdPlot,control,control1,control2,errorPlot)

        # Logica para seguir con el programa o salirse del bucle
        print("Presiona cualquier tecla para continuar, o 'esc' para salir: ", end='', flush=True)
        key_pressed = keyboard.read_event(suppress=True).name
        if key_pressed == 'esc':  # Verifica si se presionó la tecla "Esc" (valor ASCII '\x1b')
            print("\nSaliendo del programa.")
            client_socket.close()
            break
        else:
            print("\nContinuando después de presionar una tecla.")
        
        # Variable auxiliar para habilitar el reincio de la posición
        i=True

        os.system('cls')    # Limpia la consola


except KeyboardInterrupt:
    print("Interrupción del usuario. Cerrando cliente.")
    client_socket.close()

finally:
    print("Cerrando cliente")
    client_socket.close()
