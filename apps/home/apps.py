from django.apps import AppConfig
from .dht11_reader import start_reading_dht11
from .gps_reader import start_reading_gps
import io

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

class SensorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.home'

    def ready(self):
        if is_raspberrypi():
            print("Starting DHT11 reader...")
            start_reading_dht11()
            print("Starting GPS reader...")
            start_reading_gps()





