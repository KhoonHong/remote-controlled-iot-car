import time
import threading
import os
import requests

# Firebase Configuration
FIREBASE_URL = "https://iot-assignment-b634b.firebaseio.com/"

# Check if we're on a development environment (e.g., Windows)
IS_DEV = os.name == 'nt'  # 'nt' is the name for the Windows platform in Python

if IS_DEV:
    # Import from our mock module
    from apps.mocks import Adafruit_DHT
else:
    # Import the real module
    import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Assuming DHT11 is connected to GPIO4, change as needed

def store_to_firestore(temperature, humidity):
    endpoint = f"{FIREBASE_URL}/dht11_data.json"
    data = {
        'temperature': temperature,
        'humidity': humidity,
        'timestamp': {'.sv': 'timestamp'}  # Firebase server timestamp directive
    }
    response = requests.post(endpoint, json=data)
    if response.status_code != 200:
        print(f"Error storing data: {response.text}")

def read_dht11():
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            store_to_firestore(temperature, humidity)
        else:
            print("Sensor failure. Check wiring.")
        time.sleep(30)

def start_reading():
    thread = threading.Thread(target=read_dht11)
    thread.daemon = True
    thread.start()
