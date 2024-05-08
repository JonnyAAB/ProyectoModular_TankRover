#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep, time
import json

import numpy as np
import serial
import math
import npid as nPID


# Pin del motor:
# Rojo motor+
# Negro motor-
# Verde gnd
# Azul vcc encoder 3.3V
# Amarillo salida A, encoder adelante activa primero este
# Blanco salida b, encoder reversa activa primero este

# Funciones 
# ----------------------------------------------------------------------
def pose(encoder_count1, encoder_count2, tiempo_muestreo):
    global x_robot, y_robot, theta_robot, radio_rueda

    # Velocidad angular del motor en radianes por segundo
    velocidad_angular1 = (encoder_count1 / 16) * ((2 * math.pi) / tiempo_muestreo)
    velocidad_angular2 = (encoder_count2 / 16) * ((2 * math.pi) / tiempo_muestreo)

    # Velocidad lineal
    velocidad_lineal1 = velocidad_angular1 * radio_rueda
    velocidad_lineal2 = velocidad_angular2 * radio_rueda

    # Se obtiene la velocidad angular y lineal del robot
    velocidad_lineal_robot = (velocidad_lineal1 + velocidad_lineal2) / 2
    velocidad_angular_robot = (radio_rueda * (velocidad_angular2 - velocidad_angular1)) / d

    # Integrar las velocidades para obtener el cambio en la posición y la orientación del robot
    cambio_x = (radio_rueda/2) * (velocidad_angular2 + velocidad_angular1) * math.cos(theta_robot)
    cambio_y = (radio_rueda/2) * (velocidad_angular2 + velocidad_angular1) * math.sin(theta_robot)
    cambio_theta = (radio_rueda/0.1)*(velocidad_angular2 - velocidad_angular1)

    # Actualizar la posición y la orientación del robot
    x_robot += cambio_x
    y_robot += cambio_y
    theta_robot += cambio_theta

    return x_robot, y_robot, theta_robot


def actualizar_posicion(channel):
    global posicion, encoder_count
    if GPIO.input(ENCODER_A) == GPIO.HIGH:  # Cuando detecta el flanco A
        if GPIO.input(ENCODER_B) == GPIO.LOW:  # Si el flanco B esta abajo, se movió hacia adelante
            posicion -= 1
            encoder_count -= 1
        else:  # Sino pos se movió para atras
            posicion += 1
            encoder_count += 1


def actualizar_posicion2(channel):
    global posicion2, encoder_count2
    if GPIO.input(ENCODER_A2) == GPIO.HIGH:  # Cuando detecta el flanco A
        if GPIO.input(ENCODER_B2) == GPIO.LOW:  # Si el flanco B esta abajo, se movió hacia adelante
            posicion2 -= 1
            encoder_count2 -= 1
        else:  # Sino pos se movió para atras
            posicion2 += 1
            encoder_count2 += 1


def setMotor(u1, u2, direccion1, direccion2):
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
    if (u < 0):
        direccion = -1
    else:
        direccion = 1

    # Saturacion
    if (abs(u) > 100):
        u = 100
    else:
        u = abs(u)
    return u, direccion


# -----------------------------------------------------------------------

try:
    # Variables globales
    posicion, posicion2 = 0  # Posición total de los enconders
    x_robot, y_robot, theta_robot = 0  # Pose inicial del robot
    encoder_count, encoder_count2 = 0  # Contador de cada encoder para estimar pose

    # Configuración Rasp
    # -----------------------------------------------------------------------------------
    # Definición de pines BOARD
    ENCODER_A = 11
    ENCODER_B = 13
    ENCODER_A2 = 29
    ENCODER_B2 = 15
    # Configuración de Raspberry Pi GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Configurado como PullDown
    GPIO.setup(ENCODER_B, GPIO.IN)
    GPIO.setup(ENCODER_A2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Configurado como PullDown
    GPIO.setup(ENCODER_B2, GPIO.IN)

    # Configuracion que detecta flancos, bouncetiem dice que tan rapido lee el encoder
    GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=actualizar_posicion, bouncetime=100)
    GPIO.add_event_detect(ENCODER_A2, GPIO.RISING, callback=actualizar_posicion2, bouncetime=100)

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

        pdx, pdy = 3, 3  # Posición deseada en el plano x y

    except Exception:
        pd = 100
        kp = 5
        kd = 0
        tSimulacion = 10

    rein = 1
    # Inicializar listas, (tiempo,posicion,AccionControl,posicionDeseada y error)
    setMotor(0, 0, 0, 0)
    # Reinicio Variables globales
    if (rein):
        posicion, posicion2 = 0
        x_robot, y_robot, theta_robot = 0

    # Inicializar parametros control
    errorAnt1, errorAnt2 = 0
    tiempoAnterior = 0
    t = 0
    i = 1         # Para agregar el primer elemento, que la diferencia de tiempo es mucha
    d = 35        # Distancia del eje de las ruedas al punto a controlar
    R = 2.3       # Radio de la rueda dentada
    L = 1         # Distancia del centro de una llanta al centro del carrito
    t_muestreo = 0  # Tiempo de muestreo para estimación de pose

    setMotor(0, 0, 0, 0)

    # Pose inicial del robot
    p = [x_robot, y_robot, theta_robot]
    # Posición del punto adelantado del carrito
    xp = x_robot + d * math.cos(theta_robot)
    yp = y_robot + d * math.sin(theta_robot)

    # Inicializamos los pesos de la red
    neurona_x = nPID(3, 1)
    neurona_y = nPID(3, 1)

    while t < tSimulacion:  # Esto es para parar el ciclo por tiempo
        # Calculo del tiempo
        tiempoActual = time()
        deltaTiempo = tiempoActual - tiempoAnterior  # Diferencia de tiempo
        tiempoAnterior = tiempoActual  # El tiempo anterior se convierte en el actual

        # Actualizar la pose cada cierto tiempo
        t_muestreo += deltaTiempo
        if (t_muestreo >= 0.2):
            p = pose(encoder_count, encoder_count2, t_muestreo)
            xp = x_robot + d * math.cos(theta_robot)
            yp = y_robot + d * math.sin(theta_robot)
            # Reiniciar valores de muestreo
            encoder_count = 0
            encoder_count2 = 0
            t_muestreo = 0

        # Calculamos los erroes en cada eje
        error1 = pdx - xp
        error2 = pdy - yp

        # Cálculo de la integral y la derivada de los errores
        intError1 = (intError1 + error1) * (1 / t)
        dError1 = error1 - errorAnt1
        errorAnt1 = error1

        intError2 = (intError2 + error2) * (1 / t)
        dError2 = error2 - errorAnt2
        errorAnt2 = error2

        # Vectores de errores
        error_x = np.array([error1, intError1, dError1])
        error_y = np.array([error2, intError2, dError2])

        # Control PID para las coordenadas x e y
        kx = neurona_x.control_u(error_x)
        neurona_x.fit(error1, error_x)

        ky = neurona_y.control_u(error_y)
        neurona_y.fit(error2, error_y, )

        # Vector de errores combinados
        errores = np.array([kx, ky])

        # Matriz modelo de la cinemática diferencial
        matriz_modelo = np.array(
            [[np.cos(theta_robot), -d * np.sin(theta_robot)], [np.sin(theta_robot), d * np.cos(theta_robot)]])

        # Cálculo de las velocidades lineal y angular
        u = np.dot(np.linalg.inv(matriz_modelo), np.array([kx, ky]))

        v = u[0]  # Control velocidad lineal
        w = u[1]  # Control velocidad angular

        # Control de las ruedas
        wr = (2 * v + w * L) / (2 * R)
        wl = (2 * v - w * L) / (2 * R)

        # Regla de conversion newtoniana
        # 100u --- 13.14 rad/s
        #   ?  --- wl--wr
        wr = (wr * 100)/13.14
        wl = (wl * 100)/13.14

        # Imprimir control
        print("\nControl 1: ", u[0], "\nControl 2: ", u[1])

        # Parte de direccion y saturacion del control
        u1, direccion1 = DireccionSaturacion(wr)
        u2, direccion2 = DireccionSaturacion(wl)

        setMotor(u1, u2, direccion1, direccion2)

        if i == 1:
            i += 1
            t += 0
        else:
            t += deltaTiempo

        # Imprimir la posición actual del encoder
        print("\nPosición X: ", x_robot, "\nPosicion Y: ", y_robot,
              "\nPosicion deseada X: ", pdx,
			  "\nPosicion deseada Y: ", pdy)

        # Imprimir error
        print("\nError X: ", error1, "\nError Y: ", error2)

        print("\nTiempo = ", t)
        print("\n------------------------------------------------------------")

        sleep(0.1)  # Para evitar problemas de lectura de datos

    setMotor(0, 0, 0, 0)
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
