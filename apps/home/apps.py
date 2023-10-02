from django.apps import AppConfig
from .dht11_reader import start_reading
import os

class SensorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.home'

    def ready(self):
        if os.name != 'nt':
            print("Starting DHT11 reader...")
            start_reading()


class GpsDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gps_data'

    def ready(self):
        if os.name != 'nt':
            print("Starting GPS reader...")
            start_reading()