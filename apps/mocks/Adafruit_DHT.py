# This is a mock module to simulate DHT11 readings.

DHT11 = 'DHT11_MOCK'

def read(sensor, pin):
    # For the sake of mock, return some dummy values
    humidity = 55.0  # example value
    temperature = 22.5  # example value
    return humidity, temperature
