import RPi.GPIO as GPIO
from time import sleep

print("Hello World")
 
LPWM = 12
RPWM = 13
# Set the GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)

# Setting GPIO pin as output
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(LPWM, GPIO.OUT)

# Set and create a PWM Object
rpwm = GPIO.PWM(RPWM, 1000)  # 1000 Hz PWM frequency
lpwm = GPIO.PWM(LPWM, 1000)  # 1000 Hz PWM frequency

# Start PWM signal
rpwm.start(0)  # Start with 0% duty cycle
lpwm.start(0)  # Start with 0% duty cycle

try:
	while True:
		# Changin PWM duty Signal
		rpwm.ChangeDutyCycle(abs(70))  # Set motor speed
		print("rpwm")
		sleep(5)
		print("lpwm")
		rpwm.ChangeDutyCycle(abs(0))  # Set motor speed
		lpwm.ChangeDutyCycle(abs(70))  # Set motor speed
		sleep(5)
		lpwm.ChangeDutyCycle(abs(0))  # Set motor speed
except KeyboardInterrupt:
	pass
	
finally:
	rpwm.stop()
	lpwm.stop()
	GPIO.cleanup()
	print("Adios :D")	
	sleep(5)

