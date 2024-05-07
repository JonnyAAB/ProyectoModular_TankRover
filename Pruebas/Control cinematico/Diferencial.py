#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep,time
import json
import serial

# Pin del motor:
	#Rojo motor+
	#Negro motor-
	#Verde gnd
	#Azul vcc encoder 3.3V
	#Amarillo salida A, encoder adelante activa primero este
	# Blanco salida b, encoder reversa activa primero este

# Funciones 
# ----------------------------------------------------------------------
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

class OdometryCalculator:
    def __init__(self, wheel_distance):
        self.wheel_distance = wheel_distance
        self.x = 0  # Posición x del robot
        self.y = 0  # Posición y del robot
        self.theta = 0  # Orientación del robot
        self.last_time = None

    def update(self, vr, vl, current_time):
        if self.last_time is None:
            self.last_time = current_time
            return

        # Calcular el cambio en el tiempo
        dt = current_time - self.last_time

        # Calcular la velocidad lineal y angular
        v = (vr + vl) / 2
        w = (vr - vl) / self.wheel_distance

        # Calcular los cambios en la posición y orientación
        dx = v * dt * math.cos(self.theta)
        dy = v * dt * math.sin(self.theta)
        dtheta = w * dt

        # Actualizar la posición y orientación
        self.x += dx
        self.y += dy
        self.theta += dtheta

        # Mantener la orientación en el rango de [0, 2*pi)
        self.theta = self.theta % (2 * math.pi)

        # Actualizar el tiempo
        self.last_time = current_time

def ControlCinematico(pd, p, dp):
	# Reescribiendo el controlador
	R = 2.3 #Radio de la rueda dentada
	L = 18 #Distancia del centro de una llanta al centro del carrito
	D = 35 #Distancia del eje de la llanta dentada al punto a controlar

	# Ganancias de control
	kx = 0 #Para la velocidad lineal
	ky = 0 #Para la velocidad angular

	# Definir el punto que será controlado
	xp = p[0] + D * math.cos(p[3])
	yp = p[1] + D * math.sin(p[3])

	#Error entre la posición actual y la deseada
	ex = pd[0] - xp
	ey = pd[1] - yp

	#Calculamos la velocidad angular
	w = np.array([[(math.cos(p[2])/2)-(D*math.sin(p[2]))/L,],[3,4]])

	# Definición de la matriz
	A = np.array([
		[np.cos(p[2])/2 - (D*np.sin(p[2]))/L, np.cos(p[2])/2 + (D*np.sin(p[2]))/L],
		[np.sin(p[2])/2 + (D*np.cos(p[2]))/L, np.sin(p[2])/2 - (D*np.cos(p[2]))/L]
	])

	# Matriz del sistema
	B = np.array([
		[kx, 0],
		[0, ky]
	])

	# Vector de entrada
	C = np.array([ex, ey])

	# Cálculo del resultado
	w = (1/R) * np.linalg.inv(A) @ B @ C

	#Revisar distribución de motores
	wr = w[0]
	wl = w[1]

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

	# Configuración Rasp
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

	# -----------------------------------------------------------------------------------------

	# Configuracion puerto serial para la ESP32
	# ----------------------------------------------------------------------
	ser = serial.Serial('/dev/ttyUSB0', 9600)  # Reemplazar el puerto COM correcto
	# ----------------------------------------------------------------------
	# while True:
	# Datos recibidos
	try:
		pd = int(input("Ingrese posición deseada: "))
		kp = float(input("Ingrese kp: "))
		kd = float(input("Ingrese kd: "))
		tSimulacion = int(input("Ingrese tiempo simulación: "))

	except Exception:
		pd = 100
		kp = 5
		kd = 0
		tSimulacion = 10

	rein = 1
	#Inicializar listas, (tiempo,posicion,AccionControl,posicionDeseada y error)
	setMotor(0,0,0,0)
	# Reinicio Variables globales
	if(rein):
		posicion = 0
		posicion_anterior = 0
		posicion2 = 0
		posicion_anterior2 = 0
		distancia_recorrida = 0
		distancia_recorrida2 = 0
		Odometria(0,0,0,0,0)

	# Inicializar parametros control	
	errorAnt1 = 0
	errorAnt2 = 0
	tiempoAnterior = 0
	t = 0
	i=1 	# Para agregar el primer elemento, que la diferencia de tiempo es mucha
	setMotor(0,0,0,0)

	vl = 0
	vr = 0 
	theta = 0
	dt = 0

	pose = Odometria(vl,vr,theta,dt, tiempoAnterior)

	while t<tSimulacion:				#Esto es para parar el ciclo por tiempo
		#Calculo del tiempo
		tiempoActual=time()
		deltaTiempo = tiempoActual-tiempoAnterior	#Diferencia de tiempo
		tiempoAnterior = tiempoActual			# El tiempo anterior se convierte en el actual

		ControlCinematico(pd,pose,dp)
		#Calculo parte derivativa
		error1 = pd-distancia_recorrida				# Calculo del error
		dError1 = (error1-errorAnt1)/deltaTiempo		# Derivada del tiempo
		errorAnt1 = error1

		error2 = pd-distancia_recorrida2				# Calculo del error
		dError2 = (error2-errorAnt2)/deltaTiempo		# Derivada del tiempo
		errorAnt2 = error2				

		# Ley de control
		u1 = kp*error1+kd*dError1
		u2 = kp*error2+kd*dError2

		#Imprimir control
		print("\nControl 1: ", u1, "\nControl 2: ", u2)

		# Parte de direccion y saturacion del control
		u1, direccion1 = DireccionSaturacion(u1)
		u2, direccion2 = DireccionSaturacion(u2)
		
		setMotor(u1,u2,direccion1,direccion2)

		if i==1:
			i+=1
			t += 0
		else:
			t += deltaTiempo
				
		# Imprimir la posición actual del encoder
		print("\nPosición encoder 1:", distancia_recorrida, "\nPosicion encoder 2:", distancia_recorrida2, "\nPosicion deseada:", pd)

		# Imprimir error
		print("\nError1: ",error1, "\nError2: ",error2)

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
