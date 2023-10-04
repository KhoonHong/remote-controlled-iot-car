# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import camera_feed, live_camera_feed, oled_view

urlpatterns = [
    path('camera_feed/', camera_feed, name='camera_feed'),
    path('get_temperature_humidity/', views.get_temperature_humidity, name='get_temperature_humidity'),
    path('start_recording/', views.start_recording, name='start_recording'),
    path('stop_recording/', views.stop_recording, name='stop_recording'),
    path('take_screenshot/', views.take_screenshot, name='take_screenshot'),
    path('control_car_view/', views.control_car_view, name='control_car_view'),
    path('get_gps_coordinates/', views.get_gps_coordinates, name='get_gps_coordinates'),
    path('set_oled_message/', views.set_oled_message, name='set_oled_message'),
    path('close_oled_message/', views.close_oled_message, name='close_oled_message'),
    path('light_led/', views.light_led, name='light_led'),
    path('activate_buzzer/', views.activate_buzzer, name='activate_buzzer'),
    path('get_temperature_dashboard/', views.get_temperature_dashboard, name='get_temperature_dashboard'),
    path('get_sensor_data/', views.get_sensor_data, name='get_sensor_data'),
    path('check_motion_detected/', views.check_motion_detected, name='check_motion_detected'),

    path('camera/', live_camera_feed, name='live_camera_feed'),
    path('display_oled/', oled_view, name='oled_view'),
    path('map/', views.map_view, name='map_view'),
    path('dashboard/', views.index, name='dashboard_view'),

    path('', views.index, name='home'),

    # Matches any html file - keep this at the end
    re_path(r'^.*\.*', views.pages, name='pages'),
]
