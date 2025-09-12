# audio.py
# Converts stored sensor activations into tones on the buzzer

from machine import Pin, PWM
import utime
import storage

# Pin for buzzer (change if wired differently)
buzzer_pin = 15
buzzer = PWM(Pin(buzzer_pin))

# Map sensor indices to frequencies (Hz)
tone_map = {
    0: 440,   # Sensor 0 → A4
    1: 494,   # Sensor 1 → B4
    2: 523,   # Sensor 2 → C5
}

# Duration for each note (seconds)
note_duration = 0.3

def play_tone(freq, duration=note_duration):
    """Play a single tone on the buzzer."""
    if freq <= 0:
        buzzer.duty_u16(0)
        return
    buzzer.freq(freq)
    buzzer.duty_u16(30000)  # volume (0–65535)
    utime.sleep(duration)
    buzzer.duty_u16(0)
    utime.sleep(0.05)  # short pause

def play_from_storage():
    """
    Plays tones based on the most recent stored activation.
    If multiple sensors are activated, plays them in sequence.
    """
    history = storage.get_all()
    if not history:
        return
    
    last_event = history[-1]  # get most recent activation
    for sensor in last_event:
        freq = tone_map.get(sensor, 0)
        play_tone(freq)
