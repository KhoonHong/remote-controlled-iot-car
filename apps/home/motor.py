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

def motor_forward():
    #Left motor
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)  
    
    #Right motor
    GPIO.output(IN3, False)  
    GPIO.output(IN4, True)  
    
    #Main motor
    GPIO.output(ENA, True)
    GPIO.output(ENB, True)

def motor_backward():
    
    GPIO.output(IN1, True)   
    GPIO.output(IN2, False)  
    
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
    if x == 0 and y == 0:  
        motor_stop()
        return

    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360
    distance = min(math.sqrt(x**2 + y**2), 1)
    speed = int(distance * 100)
    
    print(f"Angle: {angle}, Speed: {speed}")
    print(f"Distance: {distance}, Speed: {speed}")

    # Define the motor action for each direction range:
    thresholds = [
        (22.5, motor_stop),  # stop for slight nudges
        (67.5, lambda: (motor_forward(), set_speed_left(int(speed * 0.5)), set_speed_right(speed))),  # Forward veering left
        (112.5, lambda: (motor_forward(), set_speed_left(speed), set_speed_right(speed))),  # Forward straight
        (157.5, lambda: (motor_forward(), set_speed_left(speed), set_speed_right(int(speed * 0.5)))),  # Forward veering right
        (202.5, lambda: (motor_backward(), set_speed_left(speed), set_speed_right(int(speed * 0.5)))),  # Backward veering right
        (247.5, lambda: (motor_backward(), set_speed_left(int(speed * 0.5)), set_speed_right(speed))),  # Backward veering left
        (292.5, lambda: (motor_backward(), set_speed_left(speed), set_speed_right(speed))),  # Backward straight
        (337.5, motor_stop),  # Stop near back point
        (360, motor_stop)  # Stop at zero
    ]


    for threshold, action in thresholds:
        if angle < threshold:
            action()
            break



def cleanup():
    # Stops the motors
    motor_stop()
    # Cleans up GPIO resources
    GPIO.cleanup()

# It's a good practice to handle cleanup when the script ends.
import atexit
atexit.register(cleanup)