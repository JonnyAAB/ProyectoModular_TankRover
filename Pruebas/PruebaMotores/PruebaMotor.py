import RPi.GPIO as GPIO
from time import sleep

# Pin del motor:
	#Rojo motor+
	#Negro motor-
	#Verde gnd
	#Azul vcc encoder 5V
	#Amarillo salida A, encoder adelante activa primero este
	# Blanco salida b, encoder reversa activa primero este

print("Hello World")
 
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
en_pwm = GPIO.output(EN_PWM, GPIO.HIGH) # Ambos enable en el mismo canal

# Start PWM signal
rpwm.start(0)  # Start with 0% duty cycle
lpwm.start(0)  # Start with 0% duty cycle
#en_pwm.start(100)

try:
	while True:
		# Changin PWM duty Signal
		print("rpwm")
		rpwm.ChangeDutyCycle(abs(70))  # Set motor speed 60 da 11.6V al motor y 0.3A
		sleep(3)
		print("lpwm")
		rpwm.ChangeDutyCycle(abs(00))  # Set motor speed 60 da 11.6V al motor y 0.3A
		sleep(1)
		lpwm.ChangeDutyCycle(abs(70))  # Set motor speed 60 da 11.6V al motor y 0.3A
		sleep(3)
		lpwm.ChangeDutyCycle(abs(0))  # Set motor speed 60 da 11.6V al motor y 0.3A
		sleep(1)
		
# Aqui se puchurra ctrl+C para salir, al hacer esto se ejecuta el finally
except KeyboardInterrupt:
	pass
	
finally:
	rpwm.stop()
	lpwm.stop()
	en_pwm.stop()
	GPIO.cleanup()			# Este limpia las terminales
	print("Adios :D")	
	sleep(5)

