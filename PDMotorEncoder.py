import RPi.GPIO as GPIO
from time import sleep,time

#Parte de Control
# Posición deseada encoder
pd = -80
#Ganancias
kp = .1
kd = 0.001

#Inicializar listas
tiempo=[]
pos = []

# Definición de pines
RPWM = 32
LPWM = 33
EN_PWM = 35
ENCODER_A = 11
ENCODER_B = 13

# Variables globales
posicion = 0

def actualizar_posicion(channel):
    global posicion
    if GPIO.input(ENCODER_A) == GPIO.HIGH:
        if GPIO.input(ENCODER_B) == GPIO.LOW:
            posicion += 1
        else:
            posicion -= 1
    else:
        if GPIO.input(ENCODER_B) == GPIO.HIGH:
            posicion += 1
        else:
            posicion -= 1
    print("Posición:", posicion)
    
def setMotor(direccion,u):
	if(direccion==1):
		rpwm.ChangeDutyCycle(abs(u))  # (ajusta según tus requerimientos)
		#rpwm.ChangeDutyCycle(10)  # Prueba de la funcion
		lpwm.ChangeDutyCycle(0)  # (ajusta según tus requerimientos)
	else:
		lpwm.ChangeDutyCycle(abs(u))  # (ajusta según tus requerimientos)
		rpwm.ChangeDutyCycle(0)  # (ajusta según tus requerimientos)
		#lpwm.ChangeDutyCycle(10)  # pruea de la fucnion

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
	lpwm.start(5)
	en_pwm.start(100)
	
	errorAnt = 0
	tiempoAnterior = 0
	while True:
		#Calculo del tiempo
		tiempoActual=time()
		deltaTiempo = tiempoActual-tiempoAnterior
		tiempoAnterior = tiempoActual
		
		#Calculo parte derivativa
		error = pd-posicion
		dError = (error-errorAnt)/deltaTiempo
		errorAnt = error
		
		# Ley de control
		u = kp*error+kd*dError
		
		#Saturación
		if(abs(u)>80):
			u=80
		
		direccion = 1
		if(u<0):
			direccion=-1
			
		setMotor(direccion,abs(u))
		
		pos.append(posicion)
		tiempo.append(tiempoActual)
			
		# Imprimir la posición actual del encoder
		print("Posición:", posicion)
		
		# Imprimir error
		print("Error: ",error)
		
		#Imprimir control
		print("El control es de: ",u)
		
		sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
	# Detener PWM y limpiar GPIO
	rpwm.stop()
	lpwm.stop()
	en_pwm.stop()
	GPIO.cleanup()
	with open("tiempo.txt","w") as archivo:
		for element in tiempo:
			archivo.write(str(element)+"\n")
	with open("posicion.txt","w") as archivo:
		for element in pos:
			archivo.write(str(element)+"\n")
		
	print("Programa terminado.")
	sleep(10)
