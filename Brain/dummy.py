# import sounddevice as sd
# import numpy as np

# mic_index = 1

# sd.default.device = mic_index

# # devices = sd.query_devices()
# # print(devices)

# def test_microphone(sample_rate=16000, duration=5):
#     try:
#         print(f"Recording {duration} seconds of audio...")
#         audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
#         sd.wait()  # Wait for recording to complete
#         print("Recording complete.")

#         # Calculate RMS to verify audio input
#         rms = np.sqrt(np.mean(audio**2))
#         print(f"RMS: {rms:.2f}")

#         if rms < 10:
#             print("Warning: Low RMS value. Check your microphone input.")
#         else:
#             print("Microphone input seems fine.")
#     except Exception as e:
#         print(f"Error: {e}")

# test_microphone()

import sounddevice as sd
import numpy as np

mic_index = 1  # Update with your device index
sample_rate = 16000
duration = 5

try:
    with sd.InputStream(samplerate=sample_rate, channels=1, dtype="int16", device=mic_index) as stream:
        print("Recording...")
        for _ in range(int(sample_rate / 4000 * duration)):  # Read for 'duration' seconds
            data, _ = stream.read(4000)
            print(f"Data length: {len(data)}, Min: {np.min(data)}, Max: {np.max(data)}")
except Exception as e:
    print(f"Error: {e}")


# import sounddevice as sd
# import numpy as np

# # Replace this with the correct index for CyberTrack H5
# mic_index = 1  # Example, replace with actual device index from query_devices()

# # Set default input device
# sd.default.device = mic_index

# def test_microphone(sample_rate=44100, duration=5):
#     try:
#         print(f"Recording {duration} seconds of audio...")
#         audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
#         sd.wait()  # Wait for recording to complete
#         print("Recording complete.")

#         # Calculate RMS to verify audio input
#         rms = np.sqrt(np.mean(audio**2))
#         print(f"RMS: {rms:.2f}")

#         if rms < 10:
#             print("Warning: Low RMS value. Check your microphone input.")
#         else:
#             print("Microphone input seems fine.")
#     except Exception as e:
#         print(f"Error: {e}")

# test_microphone()
