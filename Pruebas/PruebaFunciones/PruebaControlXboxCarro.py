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

def setMotor(u1,u2,direccion1,direccion2):
	# Envia los datos a la ESP32 para controlar los motores 
	data = {
            "u1": u1, "u2": u2, "direccion1": direccion1, "direccion2": direccion2
        }
	# Convierte el diccionario en una cadena JSON
	json_data = json.dumps(data)
	try:
		# Envía la cadena JSON a la ESP32 a través del puerto serial
		ser.write((json_data + "\n").encode())
		print(f"Dato JSON enviado: {json_data}")
	except Exception as e:
		print(f"Error al enviar datos: {e}")

def setValue(u,left_stick_x):
    # Stick izquierdo, eje X, -1 izquierdo 1 derecho
    # Calcular el valor absoluto del stick
    abs_left_stick_x = abs(left_stick_x)

    # Calcular un control proporcional al absoluto del stick
    control_factor = (1 - abs_left_stick_x) if abs_left_stick_x < 1 else 0

    # Calculo de la velocidad
    u1 = u * control_factor
    u2 = u * (1 - control_factor)

    return u1, u2

def normalizar_valor(valor_original):
    valor_normalizado = ((valor_original - (-1)) / (2)) * 60
    return abs(valor_normalizado)

# Inicializa Pygame
pygame.init()

# Inicializa los joysticks
pygame.joystick.init()

# Configuracion puerto serial para la ESP32
# ----------------------------------------------------------------------
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Reemplazar el puerto COM correcto
# ----------------------------------------------------------------------

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
    # Definición de pines BOARD
    ENCODER_A = 11
    ENCODER_B = 13
    ENCODER_A2 = 16
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

   
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:           # Si back es presionado se sale de la función
                    break

            elif event.type == pygame.JOYAXISMOTION:
                    if event.axis == 4:  # Gatillo izquierdo
                        left_trigger = event.value
                        u = normalizar_valor(left_trigger)
                        # # Lectura de los valores de los sticks analógicos
                        left_stick_x = joystick.get_axis(0)  # Stick izquierdo, eje X, -1 izquierdo 1 derecho
                        if u <= 0.009:
                            setMotor(0,0,0,0)
                        else:
                            u1,u2 = setValue(u,left_stick_x)
                            setMotor(u1,u2,0,0)
                        
                    elif event.axis == 5:  # Gatillo derecho
                        right_trigger = event.value
                        u = normalizar_valor(right_trigger)
                        # # Lectura de los valores de los sticks analógicos
                        left_stick_x = joystick.get_axis(0)  # Stick izquierdo, eje X, -1 izquierdo 1 derecho
                        if u <= 0.09:
                            setMotor(0, 0,1,1)
                        else:
                            u1,u2 = setValue(u,left_stick_x) 
                            setMotor(u1, u2,1,1)            

            # left_stick_y = joystick.get_axis(1)  # Stick izquierdo, eje Y, -1 arriba 1 abajo
            # right_stick_x = joystick.get_axis(2)  # Stick derecho, eje Y, -1 arriba 1 abajo
            # right_stick_y = joystick.get_axis(3)  # Stick derecho, eje X, -1 izquierdo 1 derecho

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
