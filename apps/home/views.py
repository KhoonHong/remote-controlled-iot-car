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
import firebase_admin
from firebase_admin import firestore

from django.http import StreamingHttpResponse


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
    return render(request, 'home/test.html')


def camera_feed(request):
    return StreamingHttpResponse(Camera().stream(), content_type='multipart/x-mixed-replace; boundary=frame')


def get_temperature_humidity(request):
    db = firestore.client()
    docs = db.collection('dht11_data').get()
    temperature = []
    humidity = []
    for doc in docs:
        data = doc.to_dict()
        temperature.append(data['temperature'])
        humidity.append(data['humidity'])
    
    return JsonResponse({'temperature': temperature, 'humidity': humidity})