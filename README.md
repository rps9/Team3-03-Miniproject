# Photon-to-Audio Device

This project uses a **Raspberry Pi Pico WH** with MicroPython to detect light photons from a flashlight on multiple sensors, store which sensors were activated, and convert that information into audio tones played through a piezo buzzer.

---

## Hardware

- Raspberry Pi Pico WH (SC1634)
- Freenove Pico Breakout Board (FNK0081)
- Piezo Buzzer (SameSky CPT-3095C-300)
- 10kΩ Resistor
- 2x Tactile Switches
- Light sensors (photoresistors / LDRs) connected to ADC pins

---

## File Structure

main.py # Main script (orchestrates sensing → storing → audio)
sensors.py # Handles light sensor input
storage.py # (to be added) Stores sensor activations
audio.py # (to be added) Plays tones based on stored data
README.md # Project documentation


---

## How It Works

1. **Sensing** – `sensors.py` reads values from the light sensors.
2. **Storing** – `storage.py` will save which sensors were activated.
3. **Audio** – `audio.py` will generate tones on the piezo buzzer based on the stored info.
4. **Main Loop** – `main.py` runs everything in sequence.

---

## Running the Code

1. Flash MicroPython onto the Pico.
2. Copy all project files to the Pico (using Thonny or rshell).
3. Connect light sensors to ADC pins (default: GP26, GP27).
4. Open Thonny and run:

```python
import main
main.main()

5. Shine a flashlight on the sensors to trigger detection and audio.

---

## Configuration
Change sensor pins in sensors.py (sensor_pins list).
Adjust detection threshold in sensors.py (LIGHT_THRESHOLD).
