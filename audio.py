# audio.py
# Converts sensor readings into tones on the buzzer

from machine import Pin, PWM
import utime
import storage

# Pin for buzzer (change if wired differently)
buzzer_pin = 16
buzzer = PWM(Pin(buzzer_pin))

# Tone settings: (max_value, frequency, duty)
tone_levels = [
    (1000,  1000, 50000),   # strongest beep
    (4000,   800, 40000),   # very strong
    (7000,   600, 30000),   # strong
    (10000,  500, 20000),   # medium
    (13000,  400, 15000),   # weak
]

# State tracking
last_threshold = None
last_play_time = 0
repeat_delay = 1000  # milliseconds between repeated tones if same level


def get_threshold(sensor_value):
    """Return the matching (freq, duty) for a sensor value."""
    for threshold, f, d in tone_levels:
        if sensor_value < threshold:
            return f, d, threshold
    return 0, 0, None  # silent


def play_from_storage():
    """
    Plays a tone immediately if sensor value changes to a new threshold.
    If the value stays in the same threshold, plays the tone again only
    if 1 second has passed.
    """
    global last_threshold, last_play_time

    sensor_value = storage.get_latest()
    if sensor_value is None:
        buzzer.duty_u16(0)
        return

    freq, duty, threshold = get_threshold(sensor_value)

    # No tone if above all thresholds
    if freq == 0:
        buzzer.duty_u16(0)
        last_threshold = None
        return

    now = utime.ticks_ms()

    # Case 1: new threshold → play immediately
    if threshold != last_threshold:
        buzzer.freq(freq)
        buzzer.duty_u16(duty)
        last_threshold = threshold
        last_play_time = now
        return

    # Case 2: same threshold → only play again after repeat_delay
    if utime.ticks_diff(now, last_play_time) >= repeat_delay:
        buzzer.freq(freq)
        buzzer.duty_u16(duty)
        last_play_time = now
    else:
        buzzer.duty_u16(0)  # stay quiet until next cycle
