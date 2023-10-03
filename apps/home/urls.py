# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import camera_feed, live_camera_feed

urlpatterns = [
    path('camera/', camera_feed, name='camera_feed'),
    path('get_temperature_humidity/', views.get_temperature_humidity, name='get_temperature_humidity'),
    path('start_recording/', views.start_recording, name='start_recording'),
    path('stop_recording/', views.stop_recording, name='stop_recording'),
    path('take_screenshot/', views.take_screenshot, name='take_screenshot'),
    path('control_car_view/', views.control_car_view, name='control_car_view'),
    path('live_camera_feed/', live_camera_feed, name='live_camera_feed'),
    path('', views.index, name='home'),

    # Matches any html file - keep this at the end
    re_path(r'^.*\.*', views.pages, name='pages'),
]
