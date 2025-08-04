"""
ComfyUI Geeky AudioMixer Node Package
====================================

A professional audio mixing node for ComfyUI that allows you to:
- Mix multiple audio tracks (voice, music, sound effects)
- Control volume, timing, and fade effects for each track
- Apply professional audio processing (normalization, compression, limiting)
- Export high-quality mixed audio for video workflows

Installation:
1. Copy this folder to ComfyUI/custom_nodes/ as ComfyUI_Geeky_AudioMixer
2. Install required dependencies: pip install soundfile scipy
3. Restart ComfyUI

Usage:
Perfect for combining narration, background music, and sound effects
into a single audio track for lip-sync videos or any multimedia project.
"""

import os
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from .audio_mixer_node import GeekyAudioMixer
except ImportError:
    # Fallback import method
    from audio_mixer_node import GeekyAudioMixer

# Export node mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "GeekyAudioMixer": GeekyAudioMixer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeekyAudioMixer": "🎵 Geeky AudioMixer"
}

# Package metadata
__version__ = "1.0.0"
__author__ = "Geeky AudioMixer"
__description__ = "Professional audio mixing node for ComfyUI workflows"

# Export everything for ComfyUI
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']