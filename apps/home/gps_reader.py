import time
import threading
import serial
from firebase_admin import firestore

# Setup UART communication parameters for GY-NEO6MV2 GPS module
SERIAL_PORT = "/dev/serial0"  # Change if using a different UART port
BAUD_RATE = 9600

def store_to_firestore(latitude, longitude):
    db = firestore.client()
    doc_ref = db.collection('gps_data').document()
    doc_ref.set({
        'latitude': latitude,
        'longitude': longitude,
        'timestamp': firestore.SERVER_TIMESTAMP
    })

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
