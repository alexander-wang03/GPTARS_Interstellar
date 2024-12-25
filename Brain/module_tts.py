"""
module_tts.py

This module handles Text-to-Speech (TTS) functionality for GPTARS. 

It supports both local and server-based TTS systems to convert text into audio streams, 
integrating seamlessly with other modules.
"""

import time
import requests
import os 
from datetime import datetime

from module_config import load_config

CONFIG = load_config()

start_time = time.time()

def update_tts_settings(ttsurl):
    """
    Updates TTS settings using a POST request to the specified server.

    Parameters:
    - ttsurl: The URL of the TTS server.
    """

    url = f"{ttsurl}/set_tts_settings"
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

def get_tts_stream(text_to_read, ttsurl, ttsclone):
    try:
        chunk_size = 1024

        if CONFIG['TTS']['charvoice'] and CONFIG['TTS']['ttsoption'] == "local":
            command = f'espeak-ng -s 140 -p 50 -v en-us+m3 "{text_to_read}" --stdout | sox -t wav - -c 1 -t wav - gain 0.0 reverb 30 highpass 500 lowpass 3000 | aplay'
            os.system(command)

        elif CONFIG['TTS']['charvoice'] and CONFIG['TTS']['ttsoption'] == "xttsv2":
            full_url = f"{ttsurl}/tts_stream"
            params = {
                'text': text_to_read,
                'speaker_wav': ttsclone,
                'language': "en"
            }
            headers = {'accept': 'audio/x-wav'}

            response = requests.get(full_url, params=params, headers=headers, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=chunk_size):
                yield chunk

    except Exception as e:
        print(f"Text-to-speech generation failed: {e}")

def talking(switch, start_time, talkinghead_base_url):
    switchep = f"{switch}_talking"
    if switch == "start":
        # requests.get(f"{talkinghead_base_url}/api/talkinghead/{switchep}")
        start_time = time.time()

    if switch == "stop":
        # requests.get(f"{talkinghead_base_url}/api/talkinghead/{switchep}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Processing Time: {elapsed_time}")
