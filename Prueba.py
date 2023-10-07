import RPi.GPIO as GPIO
import time

# Define the GPIO pins for PWM, direction, and enable
PWM_PIN = 13
DIR_PIN = 13
EN_PIN = 12

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)

# Set up PWM
pwm = GPIO.PWM(PWM_PIN, 1000)  # 1000 Hz PWM frequency
pwm.start(0)  # Start with 0% duty cycle

# Motor control functions
def set_motor_speed(speed):
    print("set_motor_speed funci")
    if speed >= 0:
        GPIO.output(DIR_PIN, GPIO.HIGH)  # Set direction forward
    else:
        GPIO.output(DIR_PIN, GPIO.LOW)  # Set direction backward
        pwm.ChangeDutyCycle(abs(speed))  # Set motor speed

def enable_motor():
    print("enable_motor funci")
    GPIO.output(EN_PIN, GPIO.HIGH)  # Enable the motor

def disable_motor():
    print("disable_motor funci")
    GPIO.output(EN_PIN, GPIO.LOW)  # Disable the motor

# Main code
try:
    print("hello")
    enable_motor()
    set_motor_speed(50)  # Set motor speed (0-100, positive for forward, negative for backward)
    time.sleep(5)  # Run the motor for 5 seconds

except KeyboardInterrupt:
    pass

finally:
    disable_motor()
    GPIO.cleanup()  # Cleanup GPIO on program exit
