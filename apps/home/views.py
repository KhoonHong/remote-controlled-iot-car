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


camera = Camera()

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the LED pin
LED_PIN = 20

# Set up the LED pin as an output
GPIO.setup(LED_PIN, GPIO.OUT)


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


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
