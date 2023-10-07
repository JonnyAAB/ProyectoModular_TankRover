import RPi.GPIO as GPIO
import time

# Define the GPIO pins for PWM, direction, and enable
PWMR_PIN = 13        
PWML_PIN = 12        
EN_PIN = 2

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMR_PIN, GPIO.OUT)
GPIO.setup(PWML_PIN, GPIO.OUT)
GPIO.setup(EN_PIN, GPIO.OUT)

# Set up PWM
pwmr = GPIO.PWM(PWMR_PIN, 1000)  # 1000 Hz PWM frequency
pwml = GPIO.PWM(PWML_PIN, 1000)  # 1000 Hz PWM frequency

pwmr.start(0)  # Start with 0% duty cycle
pwml.start(0)  # Start with 0% duty cycle

# Motor control functions
def set_motor_speed(speed):
    print("set_motor_speed funci")
    if speed >= 0:
        pwmr.ChangeDutyCycle(abs(speed))  # Set motor speed
        pwml.ChangeDutyCycle(abs(0))  # Set motor speed      
        # Set direction forward, don't do that, maybe cause PIN problem?
        #, no connected correctly to motor drive? :/
        
    else:
        pwmr.ChangeDutyCycle(abs(0))  # Set motor speed
        pwml.ChangeDutyCycle(abs(speed))  # Set motor speed     
        


def enable_motor():
    print("enable_motor funci")
    GPIO.output(EN_PIN, GPIO.HIGH)  # Enable the motor

def disable_motor():
    print("disable_motor funci")
    GPIO.output(EN_PIN, GPIO.LOW)  # Disable the motor

# Main code
try:
    print("hello")
    while True:
        enable_motor()
        set_motor_speed(-50)  # Set motor speed (0-100, positive for forward, negative for backward)
        time.sleep(5)  # Run the motor for 5 seconds
        set_motor_speed(50)  # Set motor speed (0-100, positive for forward, negative for backward)
        time.sleep(5)  # Run the motor for 5 seconds

except KeyboardInterrupt:
    pass

finally:
    print("bye")
    disable_motor()
    GPIO.cleanup()  # Cleanup GPIO on program exit
    time.sleep(3)
