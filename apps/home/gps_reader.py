import time
import threading
import serial
import firebase_admin
from firebase_admin import firestore

# Setup UART communication parameters for GY-NEO6MV2 GPS module
SERIAL_PORT = "/dev/serial0"  # Change if using a different UART port
BAUD_RATE = 9600

def store_to_firestore(latitude, longitude):
    try:
        db = firestore.client()
        doc_ref = db.collection('gps_data').document()
        doc_ref.set({
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
    except Exception as e:
        print(f"Error saving to Firestore: {e}")

def nmea_to_decimal(coord, direction):
    # Converts NMEA format to decimal format
    degrees = int(coord) // 100
    minutes = coord - 100*degrees
    decimals = degrees + minutes/60.0
    if direction in ['S', 'W']:
        decimals = -decimals
    return decimals

def read_gps():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
                print(f"Raw GPS Line: {line}")  # Print the raw line
                if line.startswith('$GPGLL'):
                    parts = line.split(',')
                    if len(parts) >= 5 and parts[1] and parts[3]:  # Check if parts exist and are not empty
                        latitude = nmea_to_decimal(float(parts[1]), parts[2])
                        longitude = nmea_to_decimal(float(parts[3]), parts[4])
                        print(f"Latitude: {latitude} \t Longitude: {longitude}")
                        store_to_firestore(latitude, longitude)
                    else:
                        print("Received an incomplete $GPGLL string.")
            except Exception as e:
                print(f"Error reading GPS data: {e}")
            time.sleep(10)


def start_reading_gps():
    thread = threading.Thread(target=read_gps)
    thread.daemon = True
    thread.start()
