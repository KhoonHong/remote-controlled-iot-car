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
        newdata = ser.readline()  # read a line of data from the serial port
        
        print("Reading data from gps...")
        print(newdata)
        
        if '$GPRMC' in str(newdata):  # check if the data contains the GPRMC string
            try:
                newmsg = pynmea2.parse(newdata.decode('utf-8'))  # decode and parse the data
                lat = newmsg.latitude  # get latitude
                lng = newmsg.longitude  # get longitude
                if lat == 0.0 and lng == 0.0:
                    print("No satellite data available")
                    continue
                gps = f"Latitude = {lat} and Longitude = {lng}"  # format the output
                print(gps)
                store_to_firestore(lat, lng)  # Store data to Firestore
            except pynmea2.nmea.ParseError:
                print("Error parsing NMEA sentence.")  # error handling
        time.sleep(60)  # Consider reducing or removing this sleep depending on your needs


def start_reading_gps():
    thread = threading.Thread(target=read_gps)
    thread.daemon = True
    thread.start()
