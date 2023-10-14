import RPi.GPIO as GPIO
from time import sleep

# Pin del motor:
#   Rojo motor+
#   Negro motor-
#   Verde GND
#   Azul VCC encoder 3.3V
#   Amarillo salida A, encoder adelante (activa primero este)
#   Blanco salida B, encoder reversa (activa primero este)

print("Prueba únicamente del encoder")

encoderA = 11
encoderB = 13
posicion = 0

print("Posición inicial:", posicion)

# Configuración Raspberry pines
GPIO.setmode(GPIO.BOARD)
GPIO.setup(encoderA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoderB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def actualizar_posicion(channel):
    global posicion
    lecturaSignalA = GPIO.input(encoderA)
    lecturaSignalB = GPIO.input(encoderB)

    # Determinar la dirección y sentido del giro del encoder
    if lecturaSignalA == lecturaSignalB:
        posicion += 1
    else:
        posicion -= 1

# Configurar la detección de eventos en ambos pines del encoder
GPIO.add_event_detect(encoderA, GPIO.BOTH, callback=actualizar_posicion)
GPIO.add_event_detect(encoderB, GPIO.BOTH, callback=actualizar_posicion)

try:
    while True:
        # Imprimir la posición actual del encoder
        print("Posición:", posicion)
        sleep(0.1)  # Esperar un corto período para evitar un bucle continuo

except KeyboardInterrupt:
    pass

# Limpieza de recursos GPIO al finalizar
finally:
	GPIO.cleanup()
	print("Adios :D")
	sleep(3)
