import time
import threading
import os
import firebase_admin
from firebase_admin import firestore

# Check if we're in a development environment (e.g., Windows)
IS_DEV = os.name == 'nt'  # 'nt' is the name for the Windows platform in Python

if IS_DEV:
    # Import from our mock module
    from apps.mocks import Adafruit_DHT
else:
    # Import the real module
    import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 26  # Assuming DHT11 is connected to GPIO26, change as needed

def store_to_firestore(temperature, humidity):
    try:
        db = firestore.client()
        doc_ref = db.collection('dht11_data').document()
        doc_ref.set({
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
    except Exception as e:
        print(f"Error saving to Firestore: {e}")

def read_dht11():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"Temp={temperature:0.1f}*C  Humidity={humidity:0.1f}%")
            store_to_firestore(temperature, humidity)
        else:
            print("Sensor failure. Check wiring.")
        time.sleep(30)

def start_reading_dht11():
    thread = threading.Thread(target=read_dht11)
    thread.daemon = True
    thread.start()
