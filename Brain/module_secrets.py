"""
module_secrets.py

Secrets module for GPTARS application.

This module provides functionality to handle secret or special content, specifically:
- Playing video files in fullscreen mode with optional rotation.
"""

from moviepy import VideoFileClip
import os
from pathlib import Path

def play_video_fullscreen(video_path, rotation_angle=0):
    """
    Play a video in fullscreen mode using MoviePy while maintaining aspect ratio.

    Parameters:
    - video_path (str): Path to the video file to play.
    - rotation_angle (int): Angle to rotate the video, default is 0.
    """
    BASE_DIR = Path(__file__).resolve().parent

    # Create the full path to the video
    clip_path = os.path.join(BASE_DIR, video_path)

    # Load the video file
    clip = VideoFileClip(clip_path)

    # Rotate the video if necessary
    if rotation_angle != 0:
        clip = clip.rotate(rotation_angle)

    # Play the video using MoviePy's built-in preview method
    clip.preview()

    # Close the clip to release resources
    clip.close()
