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


import io
import picamera
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


class Camera:
    def stream(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.framerate = 24
            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, format='jpeg', quality=70, use_video_port=True):
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + stream.getvalue() + b'\r\n')
                stream.seek(0)
                stream.truncate()

camera = Camera()

def gen(camera):
    return camera.stream()

def camera_feed(request):
    return StreamingHttpResponse(gen(camera), content_type='multipart/x-mixed-replace; boundary=frame')