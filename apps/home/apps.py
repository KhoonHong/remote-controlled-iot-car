from django.apps import AppConfig
from .dht11_reader import start_reading_dht11
from .gps_reader import start_reading_gps
import io
import logging

log = logging.getLogger(__name__)

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower():
                return True
    except Exception as e:
        log.error(f"Error checking Raspberry Pi: {e}")
    return False

class SensorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.home'

    def ready(self):
        if is_raspberrypi():
            try:
                log.info("Starting DHT11 reader...")
                start_reading_dht11()
            except Exception as e:
                log.error(f"Error starting DHT11 reader: {e}")

            try:
                log.info("Starting GPS reader...")
                start_reading_gps()
            except Exception as e:
                log.error(f"Error starting GPS reader: {e}")
        # pass # due to firestore limit exceeded
