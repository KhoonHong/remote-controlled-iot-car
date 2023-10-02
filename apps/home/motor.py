import RPi.GPIO as GPIO
import time
import math

# Pin definitions
IN1 = 17
IN2 = 18

IN3 = 22
IN4 = 23

ENA = 21
ENB = 24

GPIO.setwarnings(False)  # Suppress GPIO warnings

# Set up RPi.GPIO settings
GPIO.setmode(GPIO.BCM)      # Use Broadcom pin numbering
GPIO.setup(IN1, GPIO.OUT)   # Set IN1 as output
GPIO.setup(IN2, GPIO.OUT)   # Set IN2 as output
GPIO.setup(IN3, GPIO.OUT)   # Set IN2 as output
GPIO.setup(IN4, GPIO.OUT)   # Set IN2 as output
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)   # Set ENA as output


# Initialization
pwmA = GPIO.PWM(ENA, 100)  # 100Hz frequency
pwmB = GPIO.PWM(ENB, 100)

pwmA.start(0)  # Initially start with 0% duty cycle = off
pwmB.start(0)

def set_speed(speed_percentage):
    pwmA.ChangeDutyCycle(speed_percentage)
    pwmB.ChangeDutyCycle(speed_percentage)

# Motor functions
def motor_forward():
    #Left motor
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    
    #Right motor
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    
    #Main motor
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)

def motor_backward():
    
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)

def motor_stop():
    GPIO.output(ENA, False)
    GPIO.output(ENB, False)


def set_speed_left(speed_percentage):
    pwmA.ChangeDutyCycle(speed_percentage)

def set_speed_right(speed_percentage):
    pwmB.ChangeDutyCycle(speed_percentage)

def control_car(x, y):
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360
    distance = min(math.sqrt(x**2 + y**2), 1)
    speed = int(distance * 100)

    thresholds = [
        (67.5, lambda: (speed, int(speed * 0.5)), motor_forward),
        (112.5, lambda: (speed, 0), motor_forward),
        (157.5, lambda: (int(speed * 0.5), speed), motor_forward),
        (202.5, lambda: (0, speed), motor_forward),
        (247.5, lambda: (int(speed * 0.5), speed), motor_backward),
        (292.5, lambda: (speed, 0), motor_backward),
        (337.5, lambda: (speed, int(speed * 0.5)), motor_backward)
    ]

    for threshold, config, direction in thresholds:
        if angle < threshold:
            speed_left, speed_right = config()
            set_speed_left(speed_left)
            set_speed_right(speed_right)
            direction()
            break
    else:
        set_speed_left(speed)
        set_speed_right(speed)
        motor_forward()

def cleanup():
    # Stops the motors
    motor_stop()
    # Cleans up GPIO resources
    GPIO.cleanup()

# It's a good practice to handle cleanup when the script ends.
import atexit
atexit.register(cleanup)