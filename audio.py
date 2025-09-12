# audio.py
# Converts sensor readings into tones on the buzzer

from machine import Pin, PWM
import utime
import storage

# Pin for buzzer (change if wired differently)
buzzer_pin = 16
buzzer = PWM(Pin(buzzer_pin))

# Tone settings: (max_value, frequency, duty)
# Lower sensor values → more light → stronger beep
tone_levels = [
    (1000,  1000, 50000),   # strongest beep
    (4000,   800, 40000),   # very strong
    (7000,   600, 30000),   # strong
    (10000,  500, 20000),   # medium
    (13000,  400, 15000),   # weak
]

def play_from_storage():
    """
    Reads the latest sensor value from storage and plays the
    corresponding tone. If above thresholds, stays silent.
    """
    sensor_value = storage.get_latest()
    if sensor_value is None:
        buzzer.duty_u16(0)
        return

    # Default: silent
    freq = 0
    duty = 0

    # Pick tone based on thresholds
    for threshold, f, d in tone_levels:
        if sensor_value < threshold:
            freq = f
            duty = d
            break

    if freq > 0:
        buzzer.freq(freq)
        buzzer.duty_u16(duty)
        utime.sleep(1)      # play for 1 second
        buzzer.duty_u16(0)  # stop
    else:
        buzzer.duty_u16(0)  # stay silent
