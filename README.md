# Photon-to-Audio Device

This project uses a **Raspberry Pi Pico WH** with MicroPython to detect light photons from a flashlight on multiple sensors, store which sensors were activated, and convert that information into audio tones played through a piezo buzzer.

---

## Hardware

- Raspberry Pi Pico WH (SC1634)
- Freenove Pico Breakout Board (FNK0081)
- Piezo Buzzer (SameSky CPT-3095C-300)
- 10kΩ Resistor
- Light sensors (photoresistors / LDRs) connected to ADC pins

---

## File Structure

- `main.py`: Main script (orchestrates sensing → storing → audio)
- `sensors.py`: Handles light sensor input.
- `storage.py`: Stores sensor activations.
- `audio.py`: Plays tones based on stored data.
- `tests.py`: imports all of the test functions so they can be easily ran. 
- `connect_to_board.py`: detects and connects to the board (made for macos).
- `README.md`: Project documentation.
- media: holds all the media for this project .
  - `demo.png`: picture of our project.


---

## How It Works

1. **Sensing** – `sensors.py` reads values from the light sensors.
2. **Storing** – `storage.py` will save which sensors were activated.
3. **Audio** – `audio.py` will generate tones on the piezo buzzer based on the stored info.
4. **Main Loop** – `main.py` runs everything in sequence.

---

## Running the Code

1. Flash MicroPython onto the Pico.
2. Copy all project files to the Pico (running connect_to_board.py does this for you in rshell). If this does not work for you, find the pico manually using `rshell -l`, then copy each file to the board running `rshell -p PORT_YOU_JUST_GOT cp FILE_NAME.py /pyboard/FILE_NAME.py` for each file you want to add.
3. Once rshell is booted up and all of the files have been loaded onto the pico run:

```
>> import main
>> main.main()
```

4. Shine a flashlight on the sensors to trigger detection and audio.

5. Cover the light sensor to have the device play back the last few notes it recorded.

---

## Configuration
- Change sensor pins in sensors.py (sensor_pins list).
- Adjust detection threshold in sensors.py (LIGHT_THRESHOLD).

## Testing
- Run `connect_to_board.py`
- once it is done running type
```
>>> import tests
>>> tests.run_all_tests()
```

## Demo

<p align="center">
  <img src="media/demo.png" alt="Demo Screenshot" width="250"/>
</p>

### <a href="https://youtube.com/shorts/8Sd5Mo-0zUk" target="_blank">Watch the demo here</a>

