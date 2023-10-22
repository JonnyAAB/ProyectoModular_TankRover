import socket
from time import sleep,time
import json
import msvcrt
import os
import matplotlib.pyplot as plt

# IMPORTANTE #
#Hasta ahora no he podido ver como eliminar las graficas asi que se necesita realizar un comentario con el comando nano
# cd ProyectoModular
# nano ConnecionConControlRasp.py
# Comentar la funcion al final del while con un # y guardarlo con ctr+O y enter
# Por ultimo correr el programa 
# sudo python3 ConnecionConControlRasp.py

def muestraGraficas(tiempo,pos,pdPlot,control,errorPlot):
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
	plt.plot(tiempo,control, color='blue',linestyle = '-')
	plt.title("Grafica Accion de Control")
	plt.xlabel("Tiempo")
	plt.ylabel("Acción de Control")
	plt.grid(True)
	
	plt.figure(3)
	plt.plot(tiempo,errorPlot, color='blue',linestyle = '-')
	plt.title("Grafica Error")
	plt.xlabel("Tiempo")
	plt.ylabel("Error")
	plt.grid(True)
	
	#Muestra las graficas
	plt.show()
	
	#	sleep(1)
	plt.close("all")
# -----------------------------------------------------------------------

# Configura el cliente
server_host = '192.168.0.44'  # La dirección IP de la Raspberry Pi en la red local
server_port = 1342  # Puerto de escucha (debe coincidir con el puerto del servidor)

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
        
        # Datos recibidos
        # -------------------------------------------------------------------------
        # Recibir los datos del servidor
        datos_recibidos = client_socket.recv(1024).decode()

        # Convertir los datos JSON a un diccionario
        datos_dict = json.loads(datos_recibidos)

        # Acceder a los datos recibidos
        comando = datos_dict["comando"]
        parametros = datos_dict["parametros"]

        #Parte de Control
        if comando == "Graficas":
            tiempo = parametros["tiempo"]
            pos = parametros["pos"]
            pdPlot = parametros["pdPlot"]
            control = parametros["control"]
            errorPlot = parametros["errorPlot"]
        # -------------------------------------------------------------------------

        muestraGraficas(tiempo,pos,pdPlot,control,errorPlot)

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
