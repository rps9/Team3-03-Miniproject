# audio.py
# Converts sensor readings into tones on the buzzer

from machine import Pin, PWM
import utime
import storage

# Pin for buzzer (change if wired differently)
buzzer_pin = 16
buzzer = PWM(Pin(buzzer_pin))

# Tone settings: (max_value, frequency, duty)
# Frequency rises smoothly from 400 Hz (weak) up to 1000 Hz (strongest).
tone_levels = [
    (11000,  400, 15000),  # weakest
    (10000,  500, 18000),
    (9000,   600, 20000),
    (8000,   700, 24000),
    (7000,   800, 28000),
    (6000,   850, 32000),
    (5000,   900, 36000),
    (4000,   940, 40000),
    (3000,   970, 44000),
    (2000,   985, 46000),
    (1000,  1000, 50000),  # strongest
]

# State tracking
last_threshold = None
last_play_time = 0
repeat_delay = 1000  # ms
high_count = 0       # consecutive "high" readings
high_limit = 25000   # above this = "high"
high_needed = 5      # number of consecutive highs to trigger playback


def get_threshold(sensor_value):
    """Return the matching (freq, duty, threshold) for a sensor value."""
    for threshold, f, d in tone_levels:
        if sensor_value < threshold:
            return f, d, threshold
    return 0, 0, None  # silent


def play_tone(freq, duty, duration=200):
    """Play a single short tone (duration in ms)."""
    if freq > 0:
        buzzer.freq(freq)
        buzzer.duty_u16(duty)
        utime.sleep_ms(duration)
        buzzer.duty_u16(0)
        utime.sleep_ms(50)  # small gap
    else:
        buzzer.duty_u16(0)


def play_from_storage():
    """
    - Normal mode: play tones based on current sensor reading.
    - If sensor stays above `high_limit` for `high_needed` consecutive readings,
      play back the last 20 stored values (latest → oldest).
    """
    global last_threshold, last_play_time, high_count

    sensor_value = storage.get_latest()
    if sensor_value is None:
        buzzer.duty_u16(0)
        return

    # Track high-value counts
    if sensor_value > high_limit:
        high_count += 1
    else:
        high_count = 0

    # Trigger playback if high for N consecutive
    if high_count >= high_needed:
        values = storage.get_all()
        for val in values:
            f, d, _ = get_threshold(val)
            play_tone(f, d, duration=300)
        high_count = 0  # reset after playback
        return

    # --- Normal tone playback ---
    freq, duty, threshold = get_threshold(sensor_value)
    if freq == 0:
        buzzer.duty_u16(0)
        last_threshold = None
        return

    now = utime.ticks_ms()

    # Case 1: new threshold → play immediately (ignore delay)
    if threshold != last_threshold:
        play_tone(freq, duty)
        last_threshold = threshold
        last_play_time = now
        return

    # Case 2: same threshold → only play again after repeat_delay
    if utime.ticks_diff(now, last_play_time) >= repeat_delay:
        play_tone(freq, duty)
        last_play_time = now
