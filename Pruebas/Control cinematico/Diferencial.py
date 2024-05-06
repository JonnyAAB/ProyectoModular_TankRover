#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep,time
import json
import serial
import numpy as np
import math

# Pin del motor:
	#Rojo motor+
	#Negro motor-
	#Verde gnd
	#Azul vcc encoder 3.3V
	#Amarillo salida A, encoder adelante activa primero este
	# Blanco salida b, encoder reversa activa primero este

# Funciones 
# ----------------------------------------------------------------------

def InicializarRasp():
	# -----------------------------------------------------------------------------------
	# Definición de pines BOARD
	ENCODER_A = 11
	ENCODER_B = 13
	ENCODER_A2 = 29
	ENCODER_B2 = 15
	# Configuración de Raspberry Pi GPIO
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# Configurado como PullDown
	GPIO.setup(ENCODER_B, GPIO.IN)
	GPIO.setup(ENCODER_A2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# Configurado como PullDown
	GPIO.setup(ENCODER_B2, GPIO.IN)

	# Configuracion que detecta flancos, bouncetiem dice que tan rapido lee el encoder
	GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=actualizar_posicion,bouncetime= 100)
	GPIO.add_event_detect(ENCODER_A2, GPIO.RISING, callback=actualizar_posicion2,bouncetime= 100)


def actualizar_posicion(channel):
	global posicion, posicion_anterior, distancia_recorrida
	if GPIO.input(ENCODER_A) == GPIO.HIGH:	#Cuando detecta el flanco A 
		if GPIO.input(ENCODER_B) == GPIO.LOW:	#Si el flanco B esta abajo, se movió hacia adelante
			posicion -= 1
		else:					#Sino pos se movió para atras
			posicion += 1
	# Calcular la distancia recorrida desde el último cálculo
	distancia_recorrida += (100 / 40) * abs(posicion - posicion_anterior)
	# Actualizar la posición anterior para el próximo cálculo
	posicion_anterior = posicion

def actualizar_posicion2(channel):
	global posicion2, posicion_anterior2, distancia_recorrida2
	if GPIO.input(ENCODER_A2) == GPIO.HIGH:	#Cuando detecta el flanco A 
		if GPIO.input(ENCODER_B2) == GPIO.LOW:	#Si el flanco B esta abajo, se movió hacia adelante
			posicion2 -= 1
		else:					#Sino pos se movió para atras
			posicion2 += 1
	# Calcular la distancia recorrida desde el último cálculo
	distancia_recorrida2 += (100 / 40) * abs(posicion2 - posicion_anterior2)
	# Actualizar la posición anterior para el próximo cálculo
	posicion_anterior2 = posicion2

def actualizar_pose(pose):
	# Calcular los cambios en la posición (delta_x, delta_y) y la orientación delta_theta
	delta_x = (pose[0] + pose[1]) * cos(pose[2]) / 2
	delta_y = (pose[0] + pose[1]) * sin(pose[2]) / 2
	delta_theta = (pose[1] - pose[0]) / 26

	# Actualizar la pose
	x += delta_x
	y += delta_y
	theta += delta_theta
	return [x,y,theta]

def setMotor(u1,u2,direccion1,direccion2):
	# Envia los datos a la ESP32 para controlar los motores 
	data = {
            "u1": u1, "u2": u2, "direccion1": direccion1, "direccion2": direccion2
        }
	"""
		Ejemplo de envio:

		{
			"u1": 50, "u2": 50, "direccion1": 1, "direccion2": -1
		}
	"""
	# Convierte el diccionario en una cadena JSON
	json_data = json.dumps(data)
	try:
		# Envía la cadena JSON a la ESP32 a través del puerto serial
		ser.write((json_data + "\n").encode())
	except Exception as e:
		print(f"Error al enviar datos: {e}")

def DireccionSaturacion(u):
	# Cambio de dirección dependiendo la ley de control
	if(u<0):
		direccion=-1
	else:
		direccion=1

	#Saturacion
	if(abs(u)>100):
		u=100
	else:
		u=abs(u)
	return u, direccion
# -----------------------------------------------------------------------

try:
	# Variables globales
	posicion = 0
	posicion_anterior = 0
	posicion2 = 0
	posicion_anterior2 = 0
	
	distancia_recorrida = 0
	distancia_recorrida2 = 0
	theta = 0


	# Configuración Rasp
	InicializarRasp()

	# -----------------------------------------------------------------------------------------
	# Configuracion puerto serial para la ESP32
	# ----------------------------------------------------------------------
	ser = serial.Serial('/dev/ttyUSB0', 9600)  # Reemplazar el puerto COM correcto
	# ----------------------------------------------------------------------

	try:
		tSimulacion = int(input("Ingrese tiempo simulación: "))

	except Exception:
		tSimulacion = 10

	rein = 1
	i = 0

	setMotor(0,0,0,0)
	# Reinicio Variables globales
	if(rein):
		posicion = 0
		posicion_anterior = 0
		posicion2 = 0
		posicion_anterior2 = 0
		distancia_recorrida = 0
		distancia_recorrida2 = 0
		theta = 0

	# Inicializar parametros control	
	errorAnt1 = 0
	errorAnt2 = 0
	tiempoAnterior = 0
	t = 0
	i=1 	# Para agregar el primer elemento, que la diferencia de tiempo es mucha

	p = [distancia_recorrida,distancia_recorrida2,theta]

	xd = np.array([100,100,math.pi])	# xd, yd, theta_d
	p = np.array(actualizar_pose(p))	# x, y, theta
	dp = np.array([0, 0, 0])       		# Vx, Vy, Vw

	v = 0	# Velocidad lineal
	w = 0	# Velocidad Angular
	
	# Propiedades del Robot
	R = 2.3 #Radio de la rueda dentada
	L = 18 #Distancia del centro de una llanta al centro del carrito

	setMotor(0,0,0,0)

	# Ganancias de control
	kv = 0.5
	kw = 0.7

	# Propiedades simulación
	t = 0.01;       		 # Paso entre muestra
	s = tSimulacion;         # Tiempo simulación
	n = s/t;        		 # Numero de muestras

	# Inicialización Gráficas
	t_plot = np.linspace(t, s, n)
	p_plot = np.zeros((3, n))
	pp_plot = np.zeros((3, n))
	c_plot = np.zeros((2, n))
	e_plot = np.zeros((2, n))
	r_plot = np.zeros((2, n))

	# Ciclo de Iteración
	for i in range(n):
		#Calculo del tiempo
		tiempoActual=time()
		dt = tiempoActual-tiempoAnterior		#Diferencia de tiempo
		tiempoAnterior = tiempoActual			# El tiempo anterior se convierte en el actual

		# Control
		ev = np.sqrt((xd[0]-p[0])**2 + (xd[1]-p[1])**2)  # Error lineal
		theta_d = np.arctan2(xd[1]-p[1], xd[0]-p[0])
		ew = theta_d - p[2]
		ew = np.arctan2(np.sin(ew), np.cos(ew))  # Error Angular

		e_plot[:, i] = np.array([ev, ew])

		v = kv * ev  # Control velocidad lineal
		w = kw * ew  # Control velocidad angular
		c_plot[:, i] = np.array([v, w])		

		# Control Ruedas
		wr = (2*v + w*L) / (2*R)
		wl = (2*v - w*L) / (2*R)
		r_plot[:, i] = np.array([wr, wl])

		#Imprimir control
		print("\nControl 1: ", wr, "\nControl 2: ", wl)

		# Parte de direccion y saturacion del control
		u1, direccion1 = DireccionSaturacion(wr)
		u2, direccion2 = DireccionSaturacion(wl)
		
		setMotor(u1,u2,direccion1,direccion2)

		p_plot[:, i] = p  # Grafica la posición
		pp_plot[:, i] = dp  # Grafica la velocidad

		p = p + dp * t  # Paso Integración

		# Imprimir la posición actual del encoder
		print("\nPosición encoder 1:", distancia_recorrida, "\nPosicion encoder 2:", distancia_recorrida2, "\nPosicion deseada:", pd)

		# Imprimir error
		print("\nError lineal: ",ev, "\nError Angular: ",ew)

		if i==1:
			i+=1
			t += 0
		else:
			t += dt
		
		print("\nTiempo = ",t)
		print("\n------------------------------------------------------------")

		sleep(0.1)	# Para evitar problemas de lectura de datos

	setMotor(0,0,0,0)
	sleep(.1)

except Exception as e:
	setMotor(0, 0, 0, 0)
	sleep(.5)
	print(e)
	pass

finally:
	# Detener conexiones y limpiar GPIO
	ser.close()
	GPIO.cleanup()	
	print("Cerrando conexiones...")
	print("Adiós :D")
	sleep(1)
