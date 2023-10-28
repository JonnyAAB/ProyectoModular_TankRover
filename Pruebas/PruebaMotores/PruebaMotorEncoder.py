import RPi.GPIO as GPIO
from time import sleep

# Definición de pines
RPWM = 32
LPWM = 33
EN_PWM = 35
ENCODER_A = 11
ENCODER_B = 13
ENCODER_A2 = 16
ENCODER_B2 = 15
# Configuración de Raspberry Pi GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(EN_PWM, GPIO.OUT)
GPIO.setup(ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# Configurado como PullDown
GPIO.setup(ENCODER_B, GPIO.IN)
GPIO.setup(ENCODER_A2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# Configurado como PullDown
GPIO.setup(ENCODER_B2, GPIO.IN)

# Configuracion que detecta flancos, bouncetiem dice que tan rapido lee el encoder
GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=actualizar_posicion,bouncetime= 100)
GPIO.add_event_detect(ENCODER_A2, GPIO.RISING, callback=actualizar_posicion2,bouncetime= 100)
# Crear objetos PWM
rpwm = GPIO.PWM(RPWM, 1000)
lpwm = GPIO.PWM(LPWM, 1000)
en_pwm = GPIO.PWM(EN_PWM, 1000)

# Variables globales
posicion = 0
posicion2 = 0

# Iniciar PWM
rpwm.start(0)
lpwm.start(5)
en_pwm.start(100)

def actualizar_posicion(channel):
    global posicion
    if GPIO.input(ENCODER_A) == GPIO.HIGH:	#Cuando detecta el flanco A 
        if GPIO.input(ENCODER_B) == GPIO.LOW:	#Si el flanco B esta abajo, se movió hacia adelante
            posicion += 1
        else:					#Sino pos se movió para atras
            posicion -= 1

def actualizar_posicion2(channel):
    global posicion2
    if GPIO.input(ENCODER_A2) == GPIO.HIGH:	#Cuando detecta el flanco A 
        if GPIO.input(ENCODER_B2) == GPIO.LOW:	#Si el flanco B esta abajo, se movió hacia adelante
            posicion2 += 1
        else:					#Sino pos se movió para atras
            posicion2 -= 1

try:
	while True:
		mediaPosicion = (posicion + posicion2)/2

		if(mediaPosicion > 65):
			rpwm.ChangeDutyCycle(0)  # (ajusta según tus requerimientos)
			lpwm.ChangeDutyCycle(5)  # (ajusta según tus requerimientos)
		elif(mediaPosicion <0):
			# Cambiar la velocidad del motor 
			rpwm.ChangeDutyCycle(5)  # (ajusta según tus requerimientos)
			lpwm.ChangeDutyCycle(0)  # (ajusta según tus requerimientos)
		# Imprimir la posición actual del encoder
		print("Posición:", mediaPosicion)
		sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    # Detener PWM y limpiar GPIO
    rpwm.stop()
    lpwm.stop()
    en_pwm.stop()
    GPIO.cleanup()
    print("Programa terminado.")
    sleep(10)
