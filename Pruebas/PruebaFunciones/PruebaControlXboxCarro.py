import pygame
import RPi.GPIO as GPIO
from time import sleep

def actualizar_posicion(channel):
    global posicion
    if GPIO.input(ENCODER_A) == GPIO.HIGH:	#Cuando detecta el flanco A 
        if GPIO.input(ENCODER_B) == GPIO.LOW:	#Si el flanco B esta abajo, se movió hacia adelante
            posicion += 1
        else:					#Sino pos se movió para atras
            posicion -= 1
    print("Posición:", posicion)	# Imprime la posición actual

def setMotor(direccion,u):
	if(direccion==1):
		rpwm.ChangeDutyCycle(abs(u))  # ajusta según el control
		lpwm.ChangeDutyCycle(0)  # Si se mueve para adelante, entonces el lpwm es 0
	else:
		lpwm.ChangeDutyCycle(abs(u))  # ajusta según el control
		rpwm.ChangeDutyCycle(0)  # Si se mueve para atras, entonces el rpwm es 0

def normalizar_valor(valor_original):
    valor_normalizado = ((valor_original - (-1)) / (2)) * 60
    return abs(valor_normalizado)

# Inicializa Pygame
pygame.init()

# Inicializa los joysticks
pygame.joystick.init()

# Comprueba si hay joysticks disponibles
if pygame.joystick.get_count() > 0:
    # Obtiene el primer joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

try:
    # Variables globales
    posicion = 0

    # Configuración Rasp
    # -----------------------------------------------------------------------------------
    # Definición de pines del tipo BOARD
    RPWM = 32
    LPWM = 33
    EN_PWM = 35
    ENCODER_A = 11
    ENCODER_B = 13
    # Configuración de Raspberry Pi GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RPWM, GPIO.OUT)
    GPIO.setup(LPWM, GPIO.OUT)
    GPIO.setup(EN_PWM, GPIO.OUT)
    GPIO.setup(ENCODER_A, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# Configurado como PullDown
    GPIO.setup(ENCODER_B, GPIO.IN)

    # Configuracion que detecta flancos, bouncetiem dice que tan rapido lee el encoder
    GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=actualizar_posicion,bouncetime= 100)

    # Crear objetos PWM
    rpwm = GPIO.PWM(RPWM, 1000)
    lpwm = GPIO.PWM(LPWM, 1000)
    en_pwm = GPIO.PWM(EN_PWM, 1000)
    # Inicializar PWM
    rpwm.start(0)
    lpwm.start(0)
    en_pwm.start(100)
    # -----------------------------------------------------------------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 6:           # Si back es presionado se sale de la función
                    break
            
            # Lectura de los valores de los sticks analógicos
            left_stick_x = joystick.get_axis(0)  # Stick izquierdo, eje X, -1 izquierdo 1 derecho
            left_stick_y = joystick.get_axis(1)  # Stick izquierdo, eje Y, -1 arriba 1 abajo
            right_stick_x = joystick.get_axis(2)  # Stick derecho, eje Y, -1 arriba 1 abajo
            right_stick_y = joystick.get_axis(3)  # Stick derecho, eje X, -1 izquierdo 1 derecho

            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 4:  # Gatillo izquierdo
                    left_trigger = event.value
                    setMotor(0,normalizar_valor(left_trigger))
                elif event.axis == 5:  # Gatillo derecho
                    right_trigger = event.value                    
                    setMotor(1,print(normalizar_valor(right_trigger)))
                
            
        


except KeyboardInterrupt:
    pass

finally:
    # Detener PWM y limpiar GPIO
    print("Cerrando conexiones...")
    print("Adios :D")
    sleep(2)
    rpwm.stop()
    lpwm.stop()
    en_pwm.stop()
    GPIO.cleanup()
