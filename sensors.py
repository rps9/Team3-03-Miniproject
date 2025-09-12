# sensors.py
# Handles light sensor input from photoresistors (via ADC)

from machine import ADC, Pin

# Assign ADC pins here
# Placeholder: two light sensors connected to GP26 and GP27
sensor_pins = [28]  

# Create ADC objects for each sensor
adc_sensors = [ADC(Pin(pin)) for pin in sensor_pins]

# Threshold for detecting "flashlight" vs. ambient light
LIGHT_THRESHOLD = 30000   # adjust based on testing

def read_sensors():
    """
    Reads all sensors and returns a list of activated sensor indices.
    Example return: [0, 2] means sensor 0 and 2 detected strong light.
    """
    activated = []
    for i, adc in enumerate(adc_sensors):
        value = adc.read_u16()  # 16-bit reading (0–65535)
        if value > LIGHT_THRESHOLD:
            activated.append(i)
    return activated
