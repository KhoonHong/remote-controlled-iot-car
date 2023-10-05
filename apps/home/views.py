# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from .streamer import Camera
from django.http import JsonResponse
from firebase_admin import firestore
import time
from .motor import *
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
import json
from PIL import Image, ImageDraw, ImageFont
import Adafruit_SSD1306
from geopy.geocoders import Nominatim
from functools import partial
import RPi.GPIO as GPIO
from threading import Thread, Event
import threading
from datetime import datetime
from collections import defaultdict
from statistics import mean
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError

camera = Camera()

motion_detected_flag = False

# Music notes and their corresponding frequencies
NOTE_C4 = 262
NOTE_D4 = 294
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_G4 = 392
NOTE_A4 = 440
NOTE_B4 = 494
NOTE_C5 = 523
NOTE_D5 = 587
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_G5 = 784
NOTE_A5 = 880
NOTE_B5 = 988

notes = [NOTE_E4, NOTE_G4, NOTE_A4, NOTE_A4, 0,
    NOTE_A4, NOTE_B4, NOTE_C5, NOTE_C5, 0,
    NOTE_C5, NOTE_D5, NOTE_B4, NOTE_B4, 0,
    NOTE_A4, NOTE_G4, NOTE_A4, 0,

    NOTE_E4, NOTE_G4, NOTE_A4, NOTE_A4, 0,
    NOTE_A4, NOTE_B4, NOTE_C5, NOTE_C5, 0,
    NOTE_C5, NOTE_D5, NOTE_B4, NOTE_B4, 0,
    NOTE_A4, NOTE_G4, NOTE_A4, 0,

    NOTE_E4, NOTE_G4, NOTE_A4, NOTE_A4, 0,
    NOTE_A4, NOTE_C5, NOTE_D5, NOTE_D5, 0,
    NOTE_D5, NOTE_E5, NOTE_F5, NOTE_F5, 0,
    NOTE_E5, NOTE_D5, NOTE_E5, NOTE_A4, 0,

    NOTE_A4, NOTE_B4, NOTE_C5, NOTE_C5, 0,
    NOTE_D5, NOTE_E5, NOTE_A4, 0,
    NOTE_A4, NOTE_C5, NOTE_B4, NOTE_B4, 0,
    NOTE_C5, NOTE_A4, NOTE_B4, 0,

    NOTE_A4, NOTE_A4,

    NOTE_A4, NOTE_B4, NOTE_C5, NOTE_C5, 0,
    NOTE_C5, NOTE_D5, NOTE_B4, NOTE_B4, 0,
    NOTE_A4, NOTE_G4, NOTE_A4, 0,

    NOTE_E4, NOTE_G4, NOTE_A4, NOTE_A4, 0,
    NOTE_A4, NOTE_B4, NOTE_C5, NOTE_C5, 0,
    NOTE_C5, NOTE_D5, NOTE_B4, NOTE_B4, 0,
    NOTE_A4, NOTE_G4, NOTE_A4, 0,

    NOTE_E4, NOTE_G4, NOTE_A4, NOTE_A4, 0,
    NOTE_A4, NOTE_C5, NOTE_D5, NOTE_D5, 0,
    NOTE_D5, NOTE_E5, NOTE_F5, NOTE_F5, 0,
    NOTE_E5, NOTE_D5, NOTE_E5, NOTE_A4, 0,

    NOTE_A4, NOTE_B4, NOTE_C5, NOTE_C5, 0,
    NOTE_D5, NOTE_E5, NOTE_A4, 0,
    NOTE_A4, NOTE_C5, NOTE_B4, NOTE_B4, 0,
    NOTE_C5, NOTE_A4, NOTE_B4, 0,

    NOTE_E5, 0, 0, NOTE_F5, 0, 0,
    NOTE_E5, NOTE_E5, 0, NOTE_G5, 0, NOTE_E5, NOTE_D5, 0, 0,
    NOTE_D5, 0, 0, NOTE_C5, 0, 0,
    NOTE_B4, NOTE_C5, 0, NOTE_B4, 0, NOTE_A4,

    NOTE_E5, 0, 0, NOTE_F5, 0, 0,
    NOTE_E5, NOTE_E5, 0, NOTE_G5, 0, NOTE_E5, NOTE_D5, 0, 0,
    NOTE_D5, 0, 0, NOTE_C5, 0, 0,
    NOTE_B4, NOTE_C5, 0, NOTE_B4, 0, NOTE_A4]  # trimmed for brevity
durations = [125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 375, 125,

    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 375, 125,

    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 125, 250, 125,

    125, 125, 250, 125, 125,
    250, 125, 250, 125,
    125, 125, 250, 125, 125,
    125, 125, 375, 375,

    250, 125,
    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 375, 125,

    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 375, 125,

    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 250, 125, 125,
    125, 125, 125, 250, 125,

    125, 125, 250, 125, 125,
    250, 125, 250, 125,
    125, 125, 250, 125, 125,
    125, 125, 375, 375,

    250, 125, 375, 250, 125, 375,
    125, 125, 125, 125, 125, 125, 125, 125, 375,
    250, 125, 375, 250, 125, 375,
    125, 125, 125, 125, 125, 500,

    250, 125, 375, 250, 125, 375,
    125, 125, 125, 125, 125, 125, 125, 125, 375,
    250, 125, 375, 250, 125, 375,
    125, 125, 125, 125, 125, 500]  # trimmed for brevity

songSpeed = 1.0 

@login_required(login_url="/login/")
def index(request):
    latitude, longitude = None, None
    try:
        db = firestore.client()

        try:
            recent_temp, second_recent_temp = get_temperature_dashboard()
        except Exception as e:
            print(f"Error fetching temperature data: {e}")
            recent_temp, second_recent_temp = None, None

        try:
            recent_humidity, second_recent_humidity = get_humidity_dashboard()
        except Exception as e:
            print(f"Error fetching humidity data: {e}")
            recent_humidity, second_recent_humidity = None, None

        diff = (recent_temp - second_recent_temp) if recent_temp and second_recent_temp else None
        humidify_diff = (recent_humidity - second_recent_humidity) if recent_humidity and second_recent_humidity else None

        try:
            latest_doc = db.collection('gps_data').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).stream()
            for doc in latest_doc:
                data = doc.to_dict()
                geo_point = data.get('location')

                if geo_point:
                    latitude = geo_point.latitude
                    longitude = geo_point.longitude
        except Exception as e:
            print(f"Error fetching GPS data: {e}")

        location_name = get_location_by_coordinates(latitude, longitude) if latitude and longitude else (None, None)

        context = {
            'segment': 'index',
            'recent_temp': recent_temp,
            'second_recent_temp': second_recent_temp,
            'diff': diff,
            'recent_humidity': recent_humidity,
            'second_recent_humidity': second_recent_humidity,
            'humidify_diff': humidify_diff,
            "location": f"{location_name[0]}, {location_name[1]}" if location_name else None,
            "coordinates": f"{latitude:.5f}, {longitude:.5f}" if latitude and longitude else None
        }

        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
    except Exception as e:
        print(f"Error in index view: {e}")
        return HttpResponseServerError('Could not render the template.')



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def live_camera_feed(request):
    time.sleep(2)
    return render(request, 'home/camera.html')

def camera_feed(request):
    return StreamingHttpResponse(camera.stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def start_recording(request):
    camera.start_recording()
    return JsonResponse({'status': 'recording started'})

def stop_recording(request):
    camera.stop_recording()
    return JsonResponse({'status': 'recording stopped'})


def get_temperature_humidity(request):
    # db = firestore.client()
    # docs = db.collection('dht11_data').get()
    temperature = []
    humidity = []
    # for doc in docs:
    #     data = doc.to_dict()
    #     temperature.append(data['temperature'])
    #     humidity.append(data['humidity'])
    
    return JsonResponse({'temperature': temperature, 'humidity': humidity})

@csrf_exempt
def control_car_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        x = data.get('x')
        y = data.get('y')
        print(x, y)
        control_car(x, y)

        return JsonResponse({"status": "success"})
    
def take_screenshot(request):
    screenshot_path = camera.take_screenshot("my_screenshot.jpg")
    print(f"Screenshot saved to {screenshot_path}")
    return JsonResponse({'status': 'screenshot taken'})


def get_gps_coordinates(request):
    db = firestore.client()
    
    # Order by the 'timestamp' field in descending order and limit the result to one document
    latest_doc = db.collection('gps_data').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).stream()

    for doc in latest_doc:
        data = doc.to_dict()
        geo_point = data.get('location')
        
        if geo_point:
            latitude = geo_point.latitude
            longitude = geo_point.longitude
            return JsonResponse({'lat': latitude, 'lng': longitude})
    
    # Return some default values or error values if no data is found
    return JsonResponse({'lat': 0, 'lng': 0})



def map_view(request):
    return render(request, 'home/map.html')

def oled_view(request):
    return render(request, 'home/display.html')


def set_oled_message(request):
    # Initialize the OLED screen
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
    disp.begin()
    disp.clear()
    disp.display()

    # Create a blank image with a black background
    width, height = disp.width, disp.height
    image = Image.new("1", (width, height), "black")
    draw = ImageDraw.Draw(image)

    # Initialize font (default)
    font = ImageFont.load_default()

    # Clear previous drawings
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    message_type = request.POST.get('option')

    # Initialize Firestore client
    db = firestore.client()
    print(f"Message type: {message_type}")

    if message_type == 'temperature':
        query = db.collection('dht11_data').order_by('timestamp', direction=firestore.Query.DESCENDING)
        docs = query.stream()

        # Initialize temperature list
        temperatures = [doc.to_dict()['temperature'] for doc in docs]

        # Calculate metrics for display
        if not temperatures:
            print("No data available.")
        else:
            current_temp = temperatures[0]
            high_temp = max(temperatures)
            low_temp = min(temperatures)
            avg_temp = sum(temperatures) / len(temperatures)

            # Determine trend
            trend = "Stable"
            if current_temp > avg_temp:
                trend = "Up"
            elif current_temp < avg_temp:
                trend = "Down"

            # Display the data
            display_temperature_data(draw, width, height, font, disp, current_temp, high_temp, low_temp, trend, image)

    elif message_type == 'humidity':
        query = db.collection('dht11_data').order_by('timestamp', direction=firestore.Query.DESCENDING)
        docs = query.stream()

        # Initialize humidity list
        humidities = [doc.to_dict()['humidity'] for doc in docs]
        # Fetch most recent humidity value
        most_recent_humidity = humidities[0] if humidities else None

        # Display the data
        display_humidity(draw, font, width, height, disp, image, most_recent_humidity)

    elif message_type == 'location':
        print("Debug - Location message type selected.")
        db = firestore.client()  # Assuming you have imported firestore and initialized it
        
        query = db.collection('gps_data').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
        docs = query.stream()
        
        latitude, longitude = None, None
        
        for doc in docs:
            data = doc.to_dict()
            geo_point = data.get('location')
            if geo_point:
                latitude = geo_point.latitude
                longitude = geo_point.longitude

        print("Debug - Latitude:", latitude)
        print("Debug - Longitude:", longitude)
        
        if latitude is not None and longitude is not None:
            country, state = get_location_by_coordinates(latitude, longitude)
            location_name = f"{state}, {country}"
            
            display_location(draw, font, width, height, disp, image, longitude, latitude, location_name)
            
            return JsonResponse({'status': 'success', 'message': 'Location data displayed'})
        else:
            print("Debug - No GPS data available.")
            return JsonResponse({'status': 'error', 'message': 'No GPS data available'}, status=400)
    print("Message sent to OLED.")
    return JsonResponse({'status': 'success'})

def display_humidity(draw, font, width, height, disp, image, humidity):   
    # Create Header "Humidity Info"
    draw.text((10, 0), "Humidity Info", font=font, fill=255)
    
    # Draw Horizontal Line
    draw.line((0, 12, width, 12), fill=255)
    
    # Display Humidity
    text_length = draw.textlength(f"Humidity: {humidity}%", font=font)
    x_centered = (width - text_length) // 2
    draw.text((x_centered, 26), f"Humidity: {humidity}%", font=font, fill=255)
    
    # Update the display
    disp.image(image)
    disp.display()


def display_location(draw, font, width, height, disp, image, longitude, latitude, location_name):
    # Create Header "Location Info"
    draw.text((10, 0), "Location Info", font=font, fill=255)

    # Draw Horizontal Line
    draw.line((0, 12, width, 12), fill=255)

    # Draw longitude
    draw.text((10, 16), f"Longitude: {longitude}", font=font, fill=255)
    
    # Draw latitude
    draw.text((10, 26), f"Latitude:  {latitude}", font=font, fill=255)
    
    # Draw location name, centered
    text_length = draw.textlength(f"{location_name}", font=font)
    x_centered = (width - text_length) // 2
    draw.text((x_centered, 42), f"{location_name}", font=font, fill=255)

    # Update the display
    disp.image(image)
    disp.display()

def display_temperature_data(draw, width, height, font, disp, current_temp, high_temp, low_temp, trend, image):
    # Header
    draw.text((10, 0), "Temperature Data", font=font, fill=255)
    draw.line((0, 10, width, 10), fill=255)
    
    # Current Temperature, positioned at the top middle
    text_length = draw.textlength(f"Current: {current_temp}C", font=font)
    x_centered = (width - text_length) // 2
    draw.text((x_centered, 15), f"Current: {current_temp}C", font=font, fill=255)
    
    # Trend arrow, next to current temperature
    draw.text((x_centered + text_length + 5, 15), f"{trend}", font=font, fill=255)
    
    # High and Low Temperature, aligned to the left
    draw.text((10, 30), f"High: {high_temp}C", font=font, fill=255)
    draw.text((10, 40), f"Low: {low_temp}C", font=font, fill=255)
        
    # Update the display
    disp.image(image)
    disp.display()

def get_location_by_coordinates(lat, long):
    geolocator = Nominatim(user_agent="iot_assignment_khlee")
    location = geolocator.reverse((lat, long), language='en')
    address = location.raw['address']
    country = address.get('country', "")
    state = address.get('state', "")
    return country, state

def close_oled_message(request):
    # Initialize the OLED screen
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_bus=1, gpio=1)
    disp.begin()
    disp.clear()
    disp.display()

    return JsonResponse({'status': 'success', 'message': 'OLED cleared'})

@csrf_exempt
def light_led(request):   
    status = request.POST.get('status')
    # Set the GPIO mode
    GPIO.setmode(GPIO.BCM)

    # Define the LED pin
    LED_PIN = 20

    # Set up the LED pin as an output
    GPIO.setup(LED_PIN, GPIO.OUT)

    if status == 'on':
        # Turn the LED on
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        # Turn the LED off
        GPIO.output(LED_PIN, GPIO.LOW)
        # Cleanup GPIO settings
        GPIO.cleanup()
    
    return JsonResponse({'status': 'success', 'message': 'LED toggled'})

# Global variables
buzzer_playing = False
pwmBuzzer = None
stop_song_event = Event()

@csrf_exempt
def activate_buzzer(request):
    global buzzer_playing, pwmBuzzer, stop_song_event
    
    status = request.POST.get('status')
    BUZZER_PIN = 19
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    
    if pwmBuzzer is None:
        pwmBuzzer = GPIO.PWM(BUZZER_PIN, 1)
        pwmBuzzer.start(0)
        
    if status == 'on':
        stop_song_event.clear()
        song_thread = Thread(target=play_song, args=(pwmBuzzer, stop_song_event))
        song_thread.start()
    else:
        stop_song_event.set()

    return JsonResponse({'status': 'success', 'message': 'Buzzer toggled'})

def play_song(pwmBuzzer, stop_event):
    for i in range(len(notes)):
        if stop_event.is_set():
            break
        play_tone(pwmBuzzer, notes[i], durations[i])


def play_tone(pwmBuzzer, frequency, duration):
    if frequency == 0:  # A rest note
        pwmBuzzer.ChangeDutyCycle(0)
    else:
        pwmBuzzer.ChangeFrequency(frequency)
        pwmBuzzer.ChangeDutyCycle(50)  # 50% duty cycle to sound the buzzer

    time.sleep(duration * songSpeed / 1000.0)  # Convert duration from ms to s
    pwmBuzzer.ChangeDutyCycle(0)  # Silence the buzzer
    time.sleep(0.05)  # A short delay between notes

def setup_pir():
    GPIO.setmode(GPIO.BCM)
    PIR_PIN = 16
    GPIO.setup(PIR_PIN, GPIO.IN)
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)


# Global variables
last_trigger_time = 0
debounce_time = 3  # seconds
trigger_count = 0
required_triggers = 3
time_window = []  # For time-based averaging
window_size = 5  # Number of readings to consider for averaging
threshold = 2  # Number of 'True' readings required in the window to trigger


def motion_detected(channel):
    global last_trigger_time, trigger_count, time_window

    # Get the current time
    current_time = time.time()

    # Debouncing
    if current_time - last_trigger_time < debounce_time:
        return

    # Update trigger count
    trigger_count += 1

    # Update the time window for averaging
    time_window.append(True)
    if len(time_window) > window_size:
        del time_window[0]

    # Check if conditions are met to register a motion detected event
    if trigger_count >= required_triggers and sum(time_window) >= threshold:
        print("Motion Detected!")
        global motion_detected_flag
        motion_detected_flag = True

        # Reset variables
        last_trigger_time = current_time
        trigger_count = 0
        time_window = []


def check_motion_detected(request):
    global motion_detected_flag
    # Wait for motion_detected_flag to become True
    while not motion_detected_flag:
        time.sleep(1)

    # Reset the flag
    motion_detected_flag = False

    return JsonResponse({'motion_detected': True})

pir_thread = threading.Thread(target=setup_pir)
pir_thread.daemon = True
pir_thread.start()


def get_temperature_dashboard():
    try:
        # Initialize Firestore client
        db = firestore.client()
        
        # Query the database, ordering by timestamp and limiting to the 2 most recent entries
        docs = db.collection('dht11_data').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(2).stream()
        
        # Initialize list to hold temperature data
        temperatures = []
        
        # Loop through query results and store in the list
        for doc in docs:
            doc_dict = doc.to_dict()
            temperatures.append(doc_dict.get('temperature'))
        
        # Check if there are enough readings
        if len(temperatures) < 2:
            return None, None
        
        # Extract the most recent and second most recent temperatures
        return temperatures[0], temperatures[1]

    except Exception as e:
        print(f"Error retrieving temperature: {e}")


def get_humidity_dashboard():
    try:
        # Initialize Firestore client
        db = firestore.client()
        
        # Query the database, ordering by timestamp and limiting to the 2 most recent entries
        docs = db.collection('dht11_data').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(2).stream()
        
        # Initialize list to hold humidity data
        humidities = []
        
        # Loop through query results and store in the list
        for doc in docs:
            doc_dict = doc.to_dict()
            humidities.append(doc_dict.get('humidity'))
        
        # Check if there are enough readings
        if len(humidities) < 2:
            return None, None
        
        # Extract the most recent and second most recent humidity readings
        return humidities[0], humidities[1]

    except Exception as e:
        print(f"Error retrieving humidity: {e}")

def get_sensor_data(request):
    try:
        db = firestore.client()
        docs = db.collection('dht11_data').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
        
        hourly_data_humidity = defaultdict(list)
        hourly_data_temperature = defaultdict(list)

        for doc in docs:
            doc_dict = doc.to_dict()
            print(doc_dict)
            timestamp = doc_dict['timestamp']
            hour = timestamp.hour
            hourly_data_humidity[hour].append(doc_dict['humidity'])
            hourly_data_temperature[hour].append(doc_dict['temperature '])

        # Calculate mean for each hour for humidity and temperature
        hourly_mean_humidity = {hour: mean(values) for hour, values in hourly_data_humidity.items()}
        hourly_mean_temperature = {hour: mean(values) for hour, values in hourly_data_temperature.items()}

        # Convert it back to the original format
        averaged_data = [{'timestamp': datetime(year=timestamp.year, month=timestamp.month, day=timestamp.day, hour=hour).isoformat(),
                          'humidity': mean_humidity,
                          'temperature': hourly_mean_temperature.get(hour, None)} for hour, mean_humidity in hourly_mean_humidity.items()]

        return JsonResponse({"status": "success", "data": averaged_data})
    except Exception as e:
        print(f"Error fetching sensor data: {e}")
        return JsonResponse({"status": "error", "message": "Could not fetch data"})