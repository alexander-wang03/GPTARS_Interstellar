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
import requests

# === Custom Modules ===
from module_engineTrainer import train_text_classifier
from module_btcontroller import *
from module_stt import *
from module_memory import *
from module_engine import *
from module_tts import *
from module_imageSummary import *
from module_config import load_config
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
    
    # Load character data and train classifier
    read_character_content()
    train_text_classifier()

    # Measure background noise
    measure_background_noise()

    # Load the configuration
    config = load_config()
    if config['ttsoption'] == 'xttsv2':
        update_tts_settings(config)

def update_tts_settings(config):
    """
    Updates TTS settings using a POST request to the specified server.
    - `config`: Dictionary containing configuration data.
    """

    url = f"{config['ttsurl']}/set_tts_settings"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        "stream_chunk_size": 100,
        "temperature": 0.7,
        "speed": 1.1,
        "length_penalty": 1.0,
        "repetition_penalty": 1.2,
        "top_p": 0.9,
        "top_k": 40,
        "enable_text_splitting": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOAD: TTS Settings updated successfully.")
        else:
            print(f"[ERROR] Failed to update TTS settings. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[ERROR] TTS update failed: {e}")

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