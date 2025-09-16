# main.py
# Orchestrates sensor reading, data storage, and audio playback

import utime
import sensors      # handles light sensing
import storage      # stores sensor activations
import audio        # converts stored info to sound

def main():
    print("Photon-to-Audio Device Starting...")

    while True:
        # Step 1: Sense which sensors are activated
        activated = sensors.read_sensor()

        # Step 2: Store the sensor info
        storage.save(activated)

        # Step 3: Convert stored info into audio
        audio.play_from_storage()

        # Small delay to avoid spamming readings
        utime.sleep(0.5)

if __name__ == "__main__":
    main()
