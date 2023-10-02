import time
import threading
from firebase_admin import firestore
import os


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
    db = firestore.client()
    doc_ref = db.collection('dht11_data').document()
    doc_ref.set({
        'temperature': temperature,
        'humidity': humidity,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

def read_dht11():
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            store_to_firestore(temperature, humidity)
        else:
            print("Sensor failure. Check wiring.")
        time.sleep(1)

def start_reading():
    thread = threading.Thread(target=read_dht11)
    thread.daemon = True
    thread.start()
