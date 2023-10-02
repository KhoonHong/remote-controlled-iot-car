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
    
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    
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
    # Calculate the angle and distance
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360  # Convert to positive degrees
    distance = min(math.sqrt(x**2 + y**2), 1)  # Distance ranges between 0 and 1
    
    # Speed adjustment
    speed = int(distance * 100)  # Convert to percentage for PWM
    # Direction determination
    if 22.5 <= angle < 67.5:
        set_speed_left(speed)
        set_speed_right(int(speed * 0.5))
        motor_forward()
    elif 67.5 <= angle < 112.5:
        set_speed_left(speed)
        set_speed_right(0)
        motor_forward()
    elif 112.5 <= angle < 157.5:
        set_speed_left(int(speed * 0.5))
        set_speed_right(speed)
        motor_forward()
    elif 157.5 <= angle < 202.5:
        set_speed_left(0)
        set_speed_right(speed)
        motor_forward()
    elif 202.5 <= angle < 247.5:
        set_speed_left(int(speed * 0.5))
        set_speed_right(speed)
        motor_backward()
    elif 247.5 <= angle < 292.5:
        set_speed_left(speed)
        set_speed_right(0)
        motor_backward()
    elif 292.5 <= angle < 337.5:
        set_speed_left(speed)
        set_speed_right(int(speed * 0.5))
        motor_backward()
    else:
        set_speed_left(speed)
        set_speed_right(speed)
        motor_forward()