"""
app.py

Main entry point for the GPTARS application. 

Initializes modules, loads configuration, and manages key threads for functionality such as 
speech-to-text, text-to-speech, Bluetooth control, and AI response generation.
"""

# === Standard Libraries ===
import os
import sys
import threading
from datetime import datetime
import concurrent.futures

# === Custom Modules ===
from module_memory import load_character_attributes
from module_stt import measure_background_noise, set_message_callback, set_wakewordtts_callback
from module_tts import update_tts_settings
from module_config import load_config
from module_btcontroller import *
from module_main import handle_stt_message, wake_word_tts, start_stt_thread, start_bt_controller_thread

# === Constants and Globals ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)
sys.path.append(os.getcwd())

stop_event = threading.Event()
executor = concurrent.futures.ProcessPoolExecutor(max_workers=4)

# === Helper Functions ===
def init_app():
    """
    Performs initial setup for the application:
    - Prints the base directory.
    - Loads character content and training data.
    - Measures background noise.
    - Configures TTS settings if applicable.
    """
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOAD: Script running from: {BASE_DIR}")
    #print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DEBUG: init_app() called")
    
    # Load character data

    # Measure background noise
    measure_background_noise()

    # Load the configuration
    CONFIG = load_config()
    if CONFIG['TTS']['ttsoption'] == 'xttsv2':
        update_tts_settings(CONFIG['TTS']['ttsurl'])

# === Main Application Logic ===
if __name__ == "__main__":
    # Perform initial setup
    init_app()

    # Configure STT and wakeword callbacks
    set_message_callback(handle_stt_message)
    set_wakewordtts_callback(wake_word_tts)

    # Start necessary threads
    stt_thread = threading.Thread(target=start_stt_thread, name="STTThread", daemon=True)
    bt_controller_thread = threading.Thread(target=start_bt_controller_thread, name="BTControllerThread", daemon=True)

    stt_thread.start()
    bt_controller_thread.start()

    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOAD: Main program running. Press Ctrl+C to stop.")
        while True:
            pass  # Keep the main program running
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        print("\nStopping all threads and shutting down executor...")
        stop_event.set()  # Signal threads to stop
        executor.shutdown(wait=True)

        # Wait for threads to finish
        stt_thread.join()
        bt_controller_thread.join()
        print("All threads and executor stopped gracefully.")