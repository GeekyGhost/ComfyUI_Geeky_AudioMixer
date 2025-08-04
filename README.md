# 🎵 ComfyUI Geeky AudioMixer

<img width="1088" height="538" alt="Screenshot 2025-08-03 200408" src="https://github.com/user-attachments/assets/ddaa88db-fb30-4335-b99c-a10d8350f332" />


A professional-grade audio mixing node for ComfyUI that allows you to combine up to 4 audio tracks with full control over timing, volume, and effects. Perfect for creating polished audio tracks for lip-sync videos, tutorials, podcasts, or any multimedia content.

## ✨ Features

### 🎤 **Multi-Track Audio Mixing**
- **1 Required Track**: Primary audio (voice, narration, main content)
- **3 Optional Tracks**: Background music, sound effects, additional audio
- **Native ComfyUI Integration**: Uses ComfyUI's audio input system directly

### 🎛️ **Professional Controls**
- **Individual Volume Control**: 0-500% range for each track with slider + number display
- **Precise Timing**: Start time offset control (0-60 seconds) for each track
- **Fade Effects**: Customizable fade in/out (0-5 seconds) for smooth transitions
- **Master Volume**: Overall output level control (0-500%)
- **Pre-Gain Boost**: Extra amplification (0.1x-10x) for very quiet audio sources

### 🔊 **Audio Processing**
- **High-Quality Resampling**: Automatic sample rate conversion with sinc interpolation
- **Smart Normalization**: Maximizes loudness while preventing clipping (-0.1dB target)
- **Dynamic Range Compression**: Optional compression (1.0-10.0 ratio)
- **Soft Limiting**: Prevents harsh clipping (-1dB default threshold)
- **Detailed Level Metering**: Real-time RMS and peak level monitoring

### 📊 **Output Options**
- **Multiple Formats**: WAV, MP3, FLAC support
- **Sample Rates**: 8kHz to 96kHz configurable
- **Stereo Processing**: Automatic mono-to-stereo conversion
- **Timeline Mixing**: Precise audio placement on timeline

## 🚀 Installation

### Method 1: ComfyUI Manager (Recommended)
1. Open ComfyUI Manager
2. Search for "Geeky AudioMixer"
3. Click Install
4. Restart ComfyUI

### Method 2: Manual Installation
1. **Clone this repository** into your ComfyUI custom_nodes folder:
   ```bash
   cd ComfyUI/custom_nodes/
   git clone https://github.com/GeekyGhost/ComfyUI_Geeky_AudioMixer.git
   ```

2. **Install Dependencies**:
   ```bash
   cd ComfyUI_Geeky_AudioMixer
   pip install -r requirements.txt
   ```

3. **Restart ComfyUI** and the node will appear in the `audio/mixing` category.

### Requirements
- `torch` (included with ComfyUI)
- `torchaudio>=0.13.0`
- `soundfile>=0.12.1`
- `numpy>=1.21.0`
- `scipy>=1.9.0` (optional, for enhanced audio processing)

## 📖 Usage Guide

### Basic Workflow Setup

```
[TTS/Audio Generator] ──→ [🎵 Geeky AudioMixer] ──→ [Video Combine Node]
[Music Loader] ──→ [audio_2 input]           │
[SFX Loader] ──→ [audio_3 input]             │
[SFX Loader] ──→ [audio_4 input]             ▼
                                    [Mixed Audio Output]
```

### Node Inputs

#### **Required Inputs**
- **`audio_1`**: Main audio track (voice, narration, primary content)
- **`output_duration`**: Length of final mixed audio in seconds
- **`output_format`**: Export format (WAV, MP3, FLAC)
- **`sample_rate`**: Target sample rate (44100Hz recommended)

#### **Optional Audio Inputs**
- **`audio_2`**: Secondary audio (background music, ambient sounds)
- **`audio_3`**: Additional audio (sound effects, notifications)
- **`audio_4`**: Extra audio (more sound effects, voice-overs)

### Control Groups

#### **🎵 AUDIO 1 CONTROLS** (Main Track)
- **Volume**: 150% default (0-500% range)
- **Start Time**: When track begins (0-60 seconds)
- **Fade In/Out**: Smooth transitions (0-5 seconds)

#### **🎵 AUDIO 2 CONTROLS** (Background)
- **Volume**: 120% default (perfect for background music)
- **Start Time**: Sync with main track
- **Fade In/Out**: 1 second defaults for smooth music entry

#### **🎵 AUDIO 3/4 CONTROLS** (Sound Effects)
- **Volume**: 100% default (adjust as needed)
- **Start Time**: Precise timing for sound effects
- **Fade In/Out**: Quick or no fades for impact sounds

#### **🎛️ MASTER CONTROLS**
- **Master Volume**: 200% default (overall output boost)
- **Pre-Gain Boost**: 100% default (extra amplification if needed)
- **Normalization**: Enabled by default (prevents clipping)
- **Compression**: 1.0 default (no compression)
- **Limiter Threshold**: -1dB default (soft limiting)

## 🎯 Real-World Examples

### Example 1: Tutorial Video
```yaml
# Voice narration (clear and prominent)
audio_1_volume: 2.0        # 200% - loud and clear
audio_1_start_time: 0.0    # Start immediately
audio_1_fade_in: 0.2       # Quick fade in
audio_1_fade_out: 0.5      # Gentle fade out

# Background music (subtle, doesn't interfere)
audio_2_volume: 0.6        # 60% - quiet background
audio_2_start_time: 0.0    # Start with voice
audio_2_fade_in: 2.0       # Slow fade in
audio_2_fade_out: 3.0      # Slow fade out

# Notification sound effect
audio_3_volume: 1.5        # 150% - audible notification
audio_3_start_time: 5.2    # Play at 5.2 seconds
audio_3_fade_in: 0.0       # Instant
audio_3_fade_out: 0.1      # Quick fade

# Master settings
master_volume: 2.5         # 250% - loud final output
output_duration: 30.0      # 30-second video
```

### Example 2: Podcast Intro
```yaml
# Intro music (main focus initially)
audio_1_volume: 2.0
audio_1_start_time: 0.0
audio_1_fade_out: 2.0      # Fade as voice comes in

# Voice narration (starts after music intro)
audio_2_volume: 2.5        # Louder than music
audio_2_start_time: 3.0    # Start at 3 seconds
audio_2_fade_in: 1.0

# Sound effect (transition)
audio_3_volume: 1.0
audio_3_start_time: 10.0   # Transition sound

master_volume: 3.0         # Very loud output
```

### Example 3: Gaming Content
```yaml
# Game audio/voice
audio_1_volume: 1.8
audio_1_start_time: 0.0

# Background music
audio_2_volume: 0.4        # Quiet background
audio_2_start_time: 0.0

# Achievement sound
audio_3_volume: 2.0        # Loud achievement sound
audio_3_start_time: 15.5

# Victory sound
audio_4_volume: 2.5        # Very loud victory
audio_4_start_time: 28.0

pre_gain_boost: 1.5        # Extra boost for gaming audio
master_volume: 2.0
```

## 🔧 Output Information

### `mixed_audio`
The final mixed audio in ComfyUI's native audio format, ready to connect to video nodes or audio export nodes.

### `mix_info` (JSON)
Detailed information about the mixing process:
```json
{
  "tracks_loaded": 3,
  "processing_steps": [
    "Processed Audio 1 (main track)",
    "Processed Audio 2",
    "Mixed 3 tracks onto 10.0s timeline",
    "Applied master volume: 2.0",
    "Applied normalization"
  ],
  "sample_rate": 44100,
  "duration": 10.0,
  "channels": 2,
  "final_levels": {
    "rms": 0.234567,
    "peak": 0.980000,
    "rms_db": -12.6,
    "peak_db": -0.2
  }
}
```

### `total_duration`
Actual duration of the mixed audio in seconds.

### `level_meters` (JSON)
Real-time audio level information:
```json
{
  "rms_left_db": -12.3,
  "rms_right_db": -12.1,
  "peak_left_db": -0.2,
  "peak_right_db": -0.1,
  "stereo_balance": "centered"
}
```

## 🎵 Pro Tips for Best Results

### Volume Balancing
- **Voice/Main Content**: 150-250% for clarity
- **Background Music**: 40-80% to avoid overwhelming dialogue
- **Sound Effects**: 100-200% depending on impact needed
- **Master Volume**: 200-300% for loud, professional output

### Timing and Fades
- **Voice**: Short fades (0.1-0.5s) for natural speech
- **Music**: Longer fades (1-3s) for smooth transitions
- **Sound Effects**: Quick or no fades for maximum impact
- **Staggered Timing**: Offset tracks by 0.1-0.5s for natural feel

### Audio Quality Settings
- **Sample Rate**: 44.1kHz for most content, 48kHz for professional video
- **Format**: WAV for editing workflows, MP3 for final delivery
- **Normalization**: Keep enabled to prevent clipping
- **Pre-Gain Boost**: Use 1.5-3.0x for very quiet audio sources

### Common Workflow Patterns
1. **Voice + Music**: Set voice at 200%, music at 60%, master at 250%
2. **Podcast**: Voice at 250%, intro music at 150%, master at 300%
3. **Gaming**: Game audio at 180%, background music at 40%, effects at 200%
4. **Tutorial**: Voice at 200%, music at 50%, notification SFX at 150%

## 🐛 Troubleshooting

### Audio Too Quiet
**Solutions:**
- Increase `master_volume` to 3.0-4.0
- Use `pre_gain_boost` of 2.0-5.0 for very quiet sources
- Raise individual track volumes above 200%
- Check that normalization is enabled

### Audio Distorted/Clipping
**Solutions:**
- Reduce `master_volume` below 2.0
- Lower individual track volumes
- Increase `limiter_threshold` to -3dB or lower
- Enable compression with ratio 2.0-4.0

### Tracks Not Audible
**Solutions:**
- Check audio connections in ComfyUI workflow
- Verify audio file formats are supported
- Increase track volume above 100%
- Check start times aren't beyond output duration

### Sample Rate Issues
**Solutions:**
- Use 44100Hz for most content
- Check console output for resampling warnings
- Ensure all input audio has valid sample rates
- Try different resampling quality settings

### LazyAudioMap Errors
**Solutions:**
- Update ComfyUI to latest version
- Restart ComfyUI after installing node
- Check that audio input nodes are compatible
- Try connecting audio through different nodes

## 📊 Technical Details

### Supported Audio Formats
- **Input**: Any format supported by ComfyUI audio nodes
- **Output**: WAV (16/24-bit), MP3, FLAC
- **Channels**: Automatic mono-to-stereo conversion
- **Sample Rates**: 8kHz to 96kHz with high-quality resampling

### Audio Processing Pipeline
1. **Audio Extraction**: Handles ComfyUI's LazyAudioMap format
2. **Format Conversion**: Ensures consistent tensor format
3. **Resampling**: High-quality sinc interpolation when needed
4. **Volume Application**: Per-track volume adjustment
5. **Fade Processing**: Smooth fade in/out curves
6. **Timeline Mixing**: Precise sample-accurate placement
7. **Master Processing**: Volume, compression, limiting
8. **Normalization**: Loudness maximization
9. **Output Formatting**: ComfyUI-compatible audio format

### Performance Notes
- **Memory Efficient**: Processes tracks sequentially
- **High Quality**: Uses torchaudio for professional audio processing
- **Real-time Capable**: Optimized for workflow performance
- **Debug Information**: Detailed console logging for troubleshooting

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues
1. Check existing [issues](https://github.com/GeekyGhost/ComfyUI_Geeky_AudioMixer/issues)
2. Provide detailed information:
   - ComfyUI version
   - Audio node versions you're using
   - Error messages from console
   - Steps to reproduce

### Feature Requests
1. Open an [issue](https://github.com/GeekyGhost/ComfyUI_Geeky_AudioMixer/issues) with "Feature Request" label
2. Describe the feature and use case
3. Explain how it would benefit users

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Submit a pull request with clear description

### Development Setup
```bash
git clone https://github.com/GeekyGhost/ComfyUI_Geeky_AudioMixer.git
cd ComfyUI_Geeky_AudioMixer
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ComfyUI Team**: For the amazing node-based interface
- **ComfyUI Community**: For inspiration and feedback
- **Audio Processing Libraries**: PyTorch Audio team for excellent tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GeekyGhost/ComfyUI_Geeky_AudioMixer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GeekyGhost/ComfyUI_Geeky_AudioMixer/discussions)
- **Discord**: Find us in ComfyUI community servers

## 🔗 Related Projects

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - The main ComfyUI project
- [ComfyUI-VideoHelperSuite](https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite) - Video processing nodes
- [ComfyUI Audio Nodes](https://github.com/melMass/comfy_mtb) - Additional audio processing tools

---

**Made with ❤️ for the ComfyUI community**

If this node helped you create amazing content, consider giving us a ⭐ on GitHub!
