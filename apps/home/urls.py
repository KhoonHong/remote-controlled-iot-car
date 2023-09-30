# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import login_view, register_user, camera_feed, live_camera_feed

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

    path('camera/', camera_feed, name='camera_feed'),
    path('live_camera_feed/', live_camera_feed, name='live_camera_feed')

]
