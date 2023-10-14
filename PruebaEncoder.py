import RPi.GPIO as GPIO
import sys
import signal
from time import sleep

# Pin del motor:
	#Rojo motor+
	#Negro motor-
	#Verde gnd
	#Azul vcc encoder 5V
	#Amarillo salida A, encoder adelante activa primero este
	# Blanco salida b, encoder reversa activa primero este
	
print("Prueba unicamente del encoder")

encoderA = 11
encoderB = 13
posicion = 0

#Esta será la funcion que llamara de retorno la funcion add_event_detect
def leerEncoder(pinNo):
	lecturaSignalB = GPIO.input(encoderB)
	global posicion
	if(lecturaSignalB > 0):
		posicion+=1
	else:
		posicion-=1
	print("Posicion:", posicion)
		
#Esta sera la funcion para pausar el programa
def signal_handler(sig, frame):
	GPIO.cleanup()
	print("Hemos terminado")
	sleep(2)
	sys.exit(0)
	
if __name__=='__main__':
	print("Posicion inicial:", posicion)
	GPIO.setmode(GPIO.BOARD)
	
	#Definiendo los pines como entrada
	GPIO.setup(encoderA,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(encoderB,GPIO.IN)
	
	#Agregando el evento
	#GPIO.add_event_detect(encoderA, GPIO.RISING, callback=leerEncoder, bouncetime=100)
	GPIO.add_event_detect(encoderA, GPIO.RISING, callback=leerEncoder,bouncetime=50)  # Al eterlo a un ciclo vale chetos
	
	#Condiciones para pausar el programa
	signal.signal(signal.SIGINT, signal_handler)		
	signal.pause()
	
	
	
'''#Bucle donde se ejecuta todo
try:
	while True:
		if not 'event' in locals():
			GPIO.add_event_detect(encoderA, GPIO.RISING, callback=leerEncoder, bouncetime=100)
		print("Posición:", posicion)
	
except KeyboardInterrupt:
	pass
	
finally:
	GPIO.cleanup()
	print("Hemos terminado")
	sleep(5)
'''
