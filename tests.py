from machine import Pin, PWM
import time

BUZZER_PIN = 16

buz = PWM(Pin(BUZZER_PIN))
buz.duty_u16(0)  # start silent

def beep(freq=440, ms=300, duty=32768):
    """Play a single tone at freq Hz for ms milliseconds."""
    buz.freq(freq)
    buz.duty_u16(duty)     # 0..65535 — 50% duty is ~32768
    time.sleep_ms(ms)
    buz.duty_u16(0)
    time.sleep_ms(50)
def main():
    # demo: A4, C5, E5 arpeggio
    for f in (440, 523, 659):
        beep(f, 250)

    buz.deinit()

if __name__ == "__main__":
    main()
