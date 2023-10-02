import time
import threading
import serial
import requests

SERIAL_PORT = "/dev/serial0"  # Change if using a different UART port
BAUD_RATE = 9600
FIREBASE_URL = "https://iot-assignment-b634b.firebaseio.com/"

def store_to_firestore(latitude, longitude):
    endpoint = f"{FIREBASE_URL}/gps_data.json"  # Firebase uses .json extension for REST
    data = {
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': {'.sv': 'timestamp'}  # Firebase server timestamp directive
    }
    response = requests.post(endpoint, json=data)
    if response.status_code != 200:
        print(f"Error storing data: {response.text}")

def read_gps():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            line = ser.readline().decode('utf-8')
            if line.startswith('$GPGLL'):
                parts = line.split(',')
                latitude = float(parts[1])  # Convert to desired format as needed
                longitude = float(parts[3])  # Convert to desired format as needed
                store_to_firestore(latitude, longitude)
            time.sleep(30)

def start_reading():
    thread = threading.Thread(target=read_gps)
    thread.daemon = True
    thread.start()

