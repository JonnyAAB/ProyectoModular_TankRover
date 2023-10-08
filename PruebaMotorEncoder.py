import RPi.GPIO as GPIO
from time import sleep

print("Hello World")
 
LPWM = 12
RPWM = 13
Encoder_DIR_B = 2
Encoder_INT_G = 3

# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Setting GPIO pin as output
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(Encoder_DIR_B, GPIO.OUT)
#GPIO.setup(Encoder_DIR_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(Encoder_INT_G, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set and create a PWM Object
rpwm = GPIO.PWM(RPWM, 1000)  # 1000 Hz PWM frequency, cambia hay que ver la frecuencia del motor y el encoder para ajustarla
lpwm = GPIO.PWM(LPWM, 1000)  # 1000 Hz PWM frequency

# Start PWM signal
rpwm.start(0)  # Start with 0% duty cycle
lpwm.start(0)  # Start with 0% duty cycle

try:
	while True:
		# Changin PWM duty Signal
		rpwm.ChangeDutyCycle(abs(70))  # Set motor speed
		print("rpwm")
		#DIR_State = GPIO.input(Encoder_DIR_B)
		INT_State = GPIO.input(Encoder_INT_G)
		#print(f"GPIO PIN Dir {Encoder_DIR_B} state: {DIR_State}")
		print(f"GPIO PIN Int {Encoder_INT_G} state: {INT_State}")
		
		sleep(5)
		print("lpwm")
		rpwm.ChangeDutyCycle(abs(0))  # Set motor speed
		lpwm.ChangeDutyCycle(abs(70))  # Set motor speed
		sleep(5)
		lpwm.ChangeDutyCycle(abs(0))  # Set motor speed

		
# Aqui se puchurra ctrl+C para salir, al hacer esto se ejecuta el finally
except KeyboardInterrupt:
	pass
	
finally:
	rpwm.stop()
	lpwm.stop()
	GPIO.cleanup()
	print("Adios :D")	
	sleep(5)

