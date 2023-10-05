import time
import threading
import serial
import firebase_admin
import pynmea2
from firebase_admin import firestore
import os

port, ser, dataout = None, None, None

if os.name == 'nt':
    port = "COM3"  # Replace with your COM port on Windows
else:
    port = "/dev/ttyAMA0"
    ser = serial.Serial(port, baudrate=9600, timeout=1)
    dataout = pynmea2.NMEAStreamReader()

def store_to_firestore(latitude, longitude):
    try:
        db = firestore.client()
        doc_ref = db.collection('gps_data').document()
        geo_point = firestore.GeoPoint(latitude, longitude)
        doc_ref.set({
            'location': geo_point,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print("Data successfully saved to Firestore")
    except Exception as e:
        print(f"Error saving to Firestore: {e}")

def read_gps():
    while True:  # Add a continuous loop to read data
        newdata = ser.readline()
        print("Reading data from gps...")
        print(newdata)
        if '$GPRMC' in str(newdata):
            try:
                newmsg = pynmea2.parse(newdata.decode('utf-8'))
                if newmsg.is_valid:  # Check if GPS data is valid
                    lat = newmsg.latitude
                    lng = newmsg.longitude
                    gps = f"Latitude = {lat} and Longitude = {lng}"
                    print(gps)
                    store_to_firestore(lat, lng)  # Store data to Firestore
            except pynmea2.nmea.ParseError:
                print("Error parsing NMEA sentence.")
        time.sleep(60)  # Consider reducing or removing this sleep depending on your needs

def start_reading_gps():
    thread = threading.Thread(target=read_gps)
    thread.daemon = True
    thread.start()
