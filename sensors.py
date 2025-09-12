# sensors.py
# Handles light sensor input from photoresistors (via ADC)

from machine import ADC, Pin

# Assign ADC pins here
# Placeholder: two light sensors connected to GP26 and GP27
sensor_pin = 28 

# Create ADC objects for each sensor
adc_sensor = ADC(Pin(sensor_pin))

# Threshold for detecting "flashlight" vs. ambient light
LIGHT_THRESHOLD = 10000   # adjust based on testing

def read_sensor():
    """
    Reads all sensors and returns a list of activated sensor indices.
    Example return: [0, 2] means sensor 0 and 2 detected strong light.
    """
    activated = []
    value = adc_sensor.read_u16()  # 16-bit reading (0–65535)
    print(value)
    if value < LIGHT_THRESHOLD:
        activated.append(0)
    return activated
