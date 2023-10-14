import RPi.GPIO as GPIO
from time import sleep

# Pin del motor:
#   Rojo motor+
#   Negro motor-
#   Verde GND
#   Azul VCC encoder 3.3V
#   Amarillo salida A, encoder adelante (activa primero este)
#   Blanco salida B, encoder reversa (activa primero este)

#Parte Motor
#-------------------------------------------------------------------
LPWM = 32
RPWM = 33
EN_PWM = 35

# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BOARD)

# Setting GPIO pin as output
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(EN_PWM, GPIO.OUT)

#GPIO.setup(Encoder_INT_G, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set and create a PWM Object
rpwm = GPIO.PWM(RPWM, 1000)  # 1000 Hz PWM frequency, activa de motor
lpwm = GPIO.PWM(LPWM, 1000)  # 1000 Hz PWM frequency, para cambiar el sentido
en_pwm = GPIO.PWM(EN_PWM, 1000) # Ambos enable en el mismo canal

# Start PWM signal
rpwm.start(0)  # Start with 0% duty cycle
lpwm.start(0)  # Start with 0% duty cycle
en_pwm.start(100)
#-------------------------------------------------------------------

#Parte Encoder
#-------------------------------------------------------------------
print("Prueba únicamente del encoder")

encoderA = 11
encoderB = 13
posicion = 0

print("Posición inicial:", posicion)

# Configuración Raspberry pines
#GPIO.setmode(GPIO.BOARD)
GPIO.setup(encoderA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoderB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#-------------------------------------------------------------------


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
	while(True):
		print("rpwm")
		rpwm.ChangeDutyCycle(abs(70))  # Set motor speed 60 da 11.6V al motor y 0.3A
		# Imprimir la posición actual del encoder
		print("Posición:", posicion)
		sleep(0.1)  # Esperar un corto período para evitar un bucle continuo

except KeyboardInterrupt:
    pass

# Limpieza de recursos GPIO al finalizar
finally:
	rpwm.stop()
	lpwm.stop()
	en_pwm.stop()
	GPIO.cleanup()
	print("Adios :D")
	sleep(3)
