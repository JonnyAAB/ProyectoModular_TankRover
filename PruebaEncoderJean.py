import RPi.GPIO as GPIO
import sys
import signal
from time import sleep

# Pin del motor:
	#Rojo motor+
	#Negro motor-
	#Verde gnd
	#Azul vcc encoder 3.3V
	#Amarillo salida A, encoder adelante activa primero este
	# Blanco salida b, encoder reversa activa primero este
	
print("Prueba unicamente del encoder")

encoderA = 11
encoderB = 13
posicion = 0

print("Posicion inicial:", posicion)

#Configuración Raspberry pines
GPIO.setmode(GPIO.BOARD)
GPIO.setup(encoderA,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoderB,GPIO.IN)


lecturaSignalA = GPIO.input(encoderA)
lecturaSignalB = GPIO.input(encoderB)

while(True):
	print(a)
	print(b)
