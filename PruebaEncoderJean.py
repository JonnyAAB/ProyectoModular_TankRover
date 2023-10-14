import RPi.GPIO as GPIO
from time import sleep

# Definición de pines
RPWM = 32
LPWM = 33
EN_PWM = 35
ENCODER_A = 11
ENCODER_B = 13

# Variables globales
posicion = 0

def actualizar_posicion(channel):
	lecturaSignalA = GPIO.input(ENCODER_A)
	#lecturaSignalB = GPIO.input(ENCODER_B)

	# Determinar la dirección y sentido del giro del encoder
	lecturaSignalB = GPIO.input(ENCODER_B)
	print(lecturaSignalA)
	print(lecturaSignalB)
	global posicion
	if(lecturaSignalB > 0):
		posicion+=1
	else:
		posicion-=1
	print("Posicion:", posicion)

try:
    # Configuración de GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RPWM, GPIO.OUT)
    GPIO.setup(LPWM, GPIO.OUT)
    GPIO.setup(EN_PWM, GPIO.OUT)
    GPIO.setup(ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(ENCODER_B, GPIO.IN)
    GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=actualizar_posicion,bouncetime=50)  # Al meterlo a un ciclo vale cheto
    
    # Crear objetos PWM
    rpwm = GPIO.PWM(RPWM, 1000)
    lpwm = GPIO.PWM(LPWM, 1000)
    en_pwm = GPIO.PWM(EN_PWM, 1000)

    # Iniciar PWM
    rpwm.start(0)
    lpwm.start(0)
    en_pwm.start(100)

    while True:
        # Cambiar la velocidad del motor 
        rpwm.ChangeDutyCycle(70)  # (ajusta según tus requerimientos)

        # Imprimir la posición actual del encoder
        print("Posición:", posicion)
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
