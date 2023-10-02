import RPi.GPIO as GPIO
import time
import math
import atexit

# Pin definitions
IN1, IN2, IN3, IN4, ENA, ENB = 17, 18, 22, 23, 21, 24

# Suppress GPIO warnings
GPIO.setwarnings(False)

# Set up RPi.GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, IN3, IN4, ENA, ENB], GPIO.OUT)

# Initialization
pwmA, pwmB = GPIO.PWM(ENA, 100), GPIO.PWM(ENB, 100)
pwmA.start(0)
pwmB.start(0)

def set_speed(speed_percentage):
    pwmA.ChangeDutyCycle(speed_percentage)
    pwmB.ChangeDutyCycle(speed_percentage)

def motor_forward():
    GPIO.output([IN1, IN3], False)
    GPIO.output([IN2, IN4, ENA, ENB], True)

def motor_backward():
    GPIO.output([IN1, IN3, ENA, ENB], True)
    GPIO.output([IN2, IN4], False)

def motor_stop():
    GPIO.output([ENA, ENB], False)

def set_speed_left(speed_percentage):
    pwmA.ChangeDutyCycle(speed_percentage)

def set_speed_right(speed_percentage):
    pwmB.ChangeDutyCycle(speed_percentage)

def control_car(x, y):
    NEAR_CENTER_THRESHOLD = 0.0005  # This threshold can be adjusted based on the sensitivity of the joystick.

    # Check for near center values
    if abs(x) < NEAR_CENTER_THRESHOLD and abs(y) < NEAR_CENTER_THRESHOLD:
        print("Stopping motors")
        motor_stop()
        return

    # Calculate angle and distance
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360
    distance = min(math.sqrt(x**2 + y**2), 1)
    speed = int(distance * 100)

    # Map the angle to motor behaviors:

    # Forward veering left (0 to 90 degrees)
    if 0 <= angle < 90:
        motor_forward()
        set_speed_left(speed * (1 - angle/90))
        set_speed_right(speed)
        return

    # Forward veering right (90 to 180 degrees)
    if 90 <= angle < 180:
        motor_forward()
        set_speed_left(speed)
        set_speed_right(speed * (1 - (angle - 90)/90))
        return

    # Backward veering right (180 to 270 degrees)
    if 180 <= angle < 270:
        motor_backward()
        set_speed_left(speed * (angle - 180)/90)
        set_speed_right(speed)
        return

    # Backward veering left (270 to 360 degrees)
    if 270 <= angle <= 360:
        motor_backward()
        set_speed_left(speed)
        set_speed_right(speed * (1 - (angle - 270)/90))
        return


def cleanup():
    motor_stop()
    GPIO.cleanup()

# Handle cleanup when the script ends
atexit.register(cleanup)
