# sensors.py
# Handles light sensor input from photoresistor (via ADC)

from machine import ADC, Pin

# ADC pin for the single light sensor
sensor_pin = 28
adc_sensor = ADC(Pin(sensor_pin))

def read_sensor():
    """
    Reads the sensor value and returns the raw ADC value (0-65535).
    Lower values mean more light (flashlight).
    """
    value = adc_sensor.read_u16()
    print("Sensor value:", value)  # for calibration/debugging
    return value
