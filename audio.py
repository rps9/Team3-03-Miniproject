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
    (1000,   1150, 50000),  # strongest (kept)
    (2000,    1075, 46000),  # A5
    (3000,    1000, 44000),  # G5
    (4000,    925, 40000),  # very strong (kept)
    (5000,    850, 36000),  # E5
    (6000,    775, 34000),  # D5
    (7000,    700, 30000),  # strong (kept)
    (8000,    625, 26000),  # C5
    (9000,    550, 20000),  # medium (kept)
    (10000,   475, 18000),  # A4
    (11000,   400, 15000),  # weak (kept)
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
        values = values[::-1]
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

    # Case 1: new threshold → play immediately
    if threshold != last_threshold:
        buzzer.freq(freq)
        buzzer.duty_u16(duty)
        last_threshold = threshold
        last_play_time = now
        return

    # Case 2: same threshold → play only if enough time passed
    if utime.ticks_diff(now, last_play_time) >= repeat_delay:
        play_tone(freq, duty)
        last_play_time = now


# ------------------ Unit Tests ------------------
if __name__ == "__main__":
    print("Running audio.py unit tests...")

    # Test get_threshold boundaries
    f, d, t = get_threshold(500)
    assert f > 0 and t == 1000, "Value below 1000 should map to first tone"

    f, d, t = get_threshold(10500)
    assert f == 400 and t == 11000, "Value just below 11000 should match last tone"

    f, d, t = get_threshold(20000)
    assert f == 0 and t is None, "Above all thresholds should be silent"

    print("get_threshold tests passed ✅")

    # Test play_from_storage with normal values
    storage.clear()
    storage.save(500)    # should trigger lowest tone
    storage.save(2000)   # mid tone
    storage.save(9000)   # medium tone

    play_from_storage()  # Should play tone for 9000
    print("Normal playback test ran (check buzzer output).")

    # Test high_value trigger
    storage.clear()
    for _ in range(6):  # exceed high_needed
        storage.save(30000)
        play_from_storage()

    print("High-value playback sequence test ran (check buzzer output).")

    print("All audio.py tests completed ✅")
