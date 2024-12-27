"""
module_tts.py

Text-to-Speech (TTS) Module for GPTARS Application.

This module handles TTS functionality, supporting both local and server-based systems
to convert text into audio streams. 
"""

# === Standard Libraries ===
import requests
import os 
from datetime import datetime
import azure.cognitiveservices.speech as speechsdk

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
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Failed to update TTS settings. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: TTS update failed: {e}")

def get_tts_stream(text, ttsoption, azure_api_key, azure_region, ttsurl, charvoice, ttsclone):
    """
    Generate TTS audio stream for the given text using the specified TTS system.

    Parameters:
    - text (str): The text to convert into speech.
    - ttsoption (str): The TTS system to use (Azure, server-based, or local).
    - ttsurl (str): The base URL of the TTS server (for server-based TTS).
    - charvoice (bool): Flag indicating whether to use character voice for TTS.
    - ttsclone (str): The TTS speaker/voice configuration.
    """
    try:
        chunk_size = 1024

        if ttsoption == "azure":
            if not azure_api_key or not azure_region:
                raise ValueError(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Azure API key and region must be provided for ttsoption 'azure'.")
            
            # Initialize Azure Speech SDK
            speech_config = speechsdk.SpeechConfig(subscription=azure_api_key, region=azure_region)
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

            # Create SSML for advanced configuration
            ssml = f"""
            <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
                <voice name='{ttsclone}'>
                    <prosody rate="0%" pitch="0%" volume="default">
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
            
            # Perform speech synthesis and yield audio chunks
            result = synthesizer.speak_ssml_async(ssml).get()
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                audio_stream = result.audio_data_stream

                while True:
                    chunk = audio_stream.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                error_message = f"Speech synthesis canceled: {cancellation_details.reason}"
                if cancellation_details.error_details:
                    error_message += f" | Error details: {cancellation_details.error_details}"
                raise RuntimeError(error_message)
            
        # Local TTS generation using `espeak-ng`
        elif ttsoption == "local" and charvoice:
            command = (
                f'espeak-ng -s 140 -p 50 -v en-us+m3 "{text}" --stdout | '
                f'sox -t wav - -c 1 -t wav - gain 0.0 reverb 30 highpass 500 lowpass 3000 | aplay'
            )
            os.system(command)

        # Server-based TTS generation using `xttsv2`
        elif ttsoption == "xttsv2" and charvoice:
            full_url = f"{ttsurl}/tts_stream"
            params = {
                'text': text,
                'speaker_wav': ttsclone,
                'language': "en"
            }
            headers = {'accept': 'audio/x-wav'}

            response = requests.get(full_url, params=params, headers=headers, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=chunk_size):
                yield chunk

    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Text-to-speech generation failed: {e}")