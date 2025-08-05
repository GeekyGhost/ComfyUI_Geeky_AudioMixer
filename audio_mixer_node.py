import torch
import numpy as np
import torchaudio
import tempfile
import os
import time
import json
from typing import Optional, Tuple, List

class GeekyAudioMixer:
    """
    Geeky AudioMixer Node for ComfyUI - FIXED VERSION
    
    Combines up to 4 audio tracks with full control over:
    - Volume levels for each track (now properly preserved!)
    - Fade in/out effects
    - Start time offsets
    - Professional audio processing
    """
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.supported_formats = ["wav", "mp3", "flac"]
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Mandatory audio input
                "audio_1": ("AUDIO",),
                
                # Output settings
                "output_duration": ("FLOAT", {
                    "default": 10.0, "min": 1.0, "max": 300.0, "step": 0.1,
                    "display": "slider"
                }),
                "output_format": (["wav", "mp3", "flac"], {"default": "wav"}),
                "sample_rate": ("INT", {
                    "default": 44100, "min": 8000, "max": 96000, "step": 1000
                }),
                
                # === AUDIO 1 CONTROLS ===
                "audio_1_volume": ("FLOAT", {
                    "default": 1.5, "min": 0.0, "max": 5.0, "step": 0.01,
                    "display": "slider"
                }),
                "audio_1_start_time": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 60.0, "step": 0.1,
                    "display": "slider"
                }),
                "audio_1_fade_in": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 5.0, "step": 0.1,
                    "display": "slider"
                }),
                "audio_1_fade_out": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 5.0, "step": 0.1,
                    "display": "slider"
                }),
            },
            "optional": {
                # Optional audio inputs
                "audio_2": ("AUDIO",),
                "audio_3": ("AUDIO",),
                "audio_4": ("AUDIO",),
                
                # === AUDIO 2 CONTROLS ===
                "audio_2_volume": ("FLOAT", {
                    "default": 1.2, "min": 0.0, "max": 5.0, "step": 0.01,
                    "display": "slider"
                }),
                "audio_2_start_time": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 60.0, "step": 0.1,
                    "display": "slider"
                }),
                "audio_2_fade_in": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1,
                    "display": "slider"
                }),
                "audio_2_fade_out": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1,
                    "display": "slider"
                }),
                
                # === AUDIO 3 CONTROLS ===
                "audio_3_volume": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01,
                    "display": "slider"
                }),
                "audio_3_start_time": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 60.0, "step": 0.1,
                    "display": "slider"
                }),
                "audio_3_fade_in": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 5.0, "step": 0.1,
                    "display": "slider"
                }),
                "audio_3_fade_out": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 5.0, "step": 0.1,
                    "display": "slider"
                }),
                
                # === AUDIO 4 CONTROLS ===
                "audio_4_volume": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01,
                    "display": "slider"
                }),
                "audio_4_start_time": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 60.0, "step": 0.1,
                    "display": "slider"
                }),
                "audio_4_fade_in": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 5.0, "step": 0.1,
                    "display": "slider"
                }),
                "audio_4_fade_out": ("FLOAT", {
                    "default": 0.0, "min": 0.0, "max": 5.0, "step": 0.1,
                    "display": "slider"
                }),
                
                # === MASTER CONTROLS ===
                "master_volume": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 5.0, "step": 0.01,
                    "display": "slider"
                }),
                
                # === NEW NORMALIZATION OPTIONS ===
                "normalization_mode": (["off", "prevent_clipping", "full_normalize", "smart_normalize"], 
                                     {"default": "prevent_clipping"}),
                
                "compression_ratio": ("FLOAT", {
                    "default": 1.0, "min": 1.0, "max": 10.0, "step": 0.1,
                    "display": "slider"
                }),
                "limiter_threshold": ("FLOAT", {
                    "default": -1.0, "min": -20.0, "max": 0.0, "step": 0.1,
                    "display": "slider"
                }),
                
                # === LOUDNESS BOOST ===
                "pre_gain_boost": ("FLOAT", {
                    "default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1,
                    "display": "slider"
                }),
            }
        }
    
    RETURN_TYPES = ("AUDIO", "STRING", "FLOAT", "STRING")
    RETURN_NAMES = ("mixed_audio", "mix_info", "total_duration", "level_meters")
    FUNCTION = "mix_audio"
    CATEGORY = "audio/mixing"
    
    def mix_audio(self, audio_1, output_duration, output_format, sample_rate,
                  audio_1_volume, audio_1_start_time, audio_1_fade_in, audio_1_fade_out,
                  audio_2=None, audio_3=None, audio_4=None,
                  audio_2_volume=1.2, audio_2_start_time=0.0, audio_2_fade_in=1.0, audio_2_fade_out=1.0,
                  audio_3_volume=1.0, audio_3_start_time=0.0, audio_3_fade_in=0.0, audio_3_fade_out=0.0,
                  audio_4_volume=1.0, audio_4_start_time=0.0, audio_4_fade_in=0.0, audio_4_fade_out=0.0,
                  master_volume=1.0, normalization_mode="prevent_clipping", compression_ratio=1.0, 
                  limiter_threshold=-1.0, pre_gain_boost=1.0):
        """
        Main audio mixing function - FIXED to preserve volume relationships!
        """
        try:
            # Prepare track configurations
            tracks = []
            mix_info = {"tracks_loaded": 0, "processing_steps": [], "warnings": []}
            
            print(f"\n🎛️ STARTING AUDIO MIX with normalization_mode: {normalization_mode}")
            
            # Process Audio 1 (mandatory)
            track_1 = self.process_audio_track(
                audio_1, "Audio 1", audio_1_volume, audio_1_start_time, 
                audio_1_fade_in, audio_1_fade_out, sample_rate, output_duration
            )
            if track_1 is not None:
                tracks.append(track_1)
                mix_info["tracks_loaded"] += 1
                mix_info["processing_steps"].append("Processed Audio 1 (main track)")
            
            # Process Audio 2 (optional)
            if audio_2 is not None:
                track_2 = self.process_audio_track(
                    audio_2, "Audio 2", audio_2_volume, audio_2_start_time,
                    audio_2_fade_in, audio_2_fade_out, sample_rate, output_duration
                )
                if track_2 is not None:
                    tracks.append(track_2)
                    mix_info["tracks_loaded"] += 1
                    mix_info["processing_steps"].append("Processed Audio 2")
            
            # Process Audio 3 (optional)
            if audio_3 is not None:
                track_3 = self.process_audio_track(
                    audio_3, "Audio 3", audio_3_volume, audio_3_start_time,
                    audio_3_fade_in, audio_3_fade_out, sample_rate, output_duration
                )
                if track_3 is not None:
                    tracks.append(track_3)
                    mix_info["tracks_loaded"] += 1
                    mix_info["processing_steps"].append("Processed Audio 3")
            
            # Process Audio 4 (optional)
            if audio_4 is not None:
                track_4 = self.process_audio_track(
                    audio_4, "Audio 4", audio_4_volume, audio_4_start_time,
                    audio_4_fade_in, audio_4_fade_out, sample_rate, output_duration
                )
                if track_4 is not None:
                    tracks.append(track_4)
                    mix_info["tracks_loaded"] += 1
                    mix_info["processing_steps"].append("Processed Audio 4")
            
            if not tracks:
                print("Warning: No valid audio tracks found")
                # Return silent audio instead of error
                silent_audio = torch.zeros(1, 2, int(sample_rate * output_duration), dtype=torch.float32)
                return (
                    {"waveform": silent_audio, "sample_rate": sample_rate},
                    json.dumps({"warning": "No valid audio tracks", "tracks_loaded": 0}),
                    output_duration,
                    json.dumps({"rms_left_db": -60, "rms_right_db": -60, "peak_left_db": -60, "peak_right_db": -60})
                )
            
            # Mix all tracks together (preserving relative volumes!)
            mixed_audio = self.mix_tracks(tracks, output_duration, sample_rate)
            mix_info["processing_steps"].append(f"Mixed {len(tracks)} tracks with preserved volume relationships")
            
            # Show levels BEFORE master volume and normalization
            pre_rms = torch.sqrt(torch.mean(mixed_audio ** 2))
            pre_peak = torch.max(torch.abs(mixed_audio))
            print(f"\n📊 LEVELS AFTER MIXING (before master processing):")
            print(f"   RMS: {pre_rms:.6f} ({20 * torch.log10(pre_rms + 1e-10):.1f} dB)")
            print(f"   Peak: {pre_peak:.6f} ({20 * torch.log10(pre_peak + 1e-10):.1f} dB)")
            
            # Apply pre-gain boost first (before other processing)
            if pre_gain_boost != 1.0:
                mixed_audio = mixed_audio * pre_gain_boost
                mix_info["processing_steps"].append(f"Applied pre-gain boost: {pre_gain_boost}x")
                print(f"🔊 Pre-gain boost applied: {pre_gain_boost}x")
            
            # Apply master volume
            mixed_audio = mixed_audio * master_volume
            mix_info["processing_steps"].append(f"Applied master volume: {master_volume}")
            print(f"🔊 Master volume applied: {master_volume}x")
            
            # Show levels after master volume
            master_rms = torch.sqrt(torch.mean(mixed_audio ** 2))
            master_peak = torch.max(torch.abs(mixed_audio))
            print(f"\n📊 LEVELS AFTER MASTER VOLUME:")
            print(f"   RMS: {master_rms:.6f} ({20 * torch.log10(master_rms + 1e-10):.1f} dB)")
            print(f"   Peak: {master_peak:.6f} ({20 * torch.log10(master_peak + 1e-10):.1f} dB)")
            
            # NEW: Apply intelligent normalization based on mode
            mixed_audio = self.apply_smart_normalization(mixed_audio, normalization_mode, mix_info)
            
            # Apply post-processing
            if compression_ratio > 1.0:
                mixed_audio = self.apply_compression(mixed_audio, compression_ratio)
                mix_info["processing_steps"].append(f"Applied compression (ratio: {compression_ratio})")
            
            if limiter_threshold > -20.0:
                mixed_audio = self.apply_limiter(mixed_audio, limiter_threshold)
                mix_info["processing_steps"].append(f"Applied limiter (threshold: {limiter_threshold}dB)")
            
            # Final level check
            final_rms = torch.sqrt(torch.mean(mixed_audio ** 2))
            final_peak = torch.max(torch.abs(mixed_audio))
            mix_info["final_levels"] = {
                "rms": float(final_rms),
                "peak": float(final_peak),
                "rms_db": float(20 * torch.log10(final_rms + 1e-10)),
                "peak_db": float(20 * torch.log10(final_peak + 1e-10))
            }
            print(f"\n🎵 FINAL LEVELS:")
            print(f"   RMS: {final_rms:.6f} ({20 * torch.log10(final_rms + 1e-10):.1f} dB)")
            print(f"   Peak: {final_peak:.6f} ({20 * torch.log10(final_peak + 1e-10):.1f} dB)")
            
            # Generate level meters
            level_meters = self.generate_level_meters(mixed_audio)
            
            # Calculate actual duration
            actual_duration = mixed_audio.shape[2] / sample_rate
            
            # Compile mix information
            mix_info.update({
                "sample_rate": sample_rate,
                "format": output_format,
                "duration": actual_duration,
                "channels": mixed_audio.shape[1],
                "master_volume": master_volume,
                "pre_gain_boost": pre_gain_boost,
                "normalization_mode": normalization_mode
            })
            
            # Safety clipping check to prevent harsh clipping
            if torch.max(torch.abs(mixed_audio)) > 1.0:
                print("⚠️  WARNING: Audio levels above 1.0, applying safety limiting")
                mixed_audio = torch.clamp(mixed_audio, -0.99, 0.99)
                mix_info["processing_steps"].append("Applied safety limiting (levels exceeded 1.0)")
            
            # Convert to ComfyUI audio format (waveform, sample_rate)
            # Ensure proper batch dimension for output
            if len(mixed_audio.shape) == 2:
                mixed_audio = mixed_audio.unsqueeze(0)  # Add batch dimension
            
            comfy_audio = {"waveform": mixed_audio, "sample_rate": sample_rate}
            
            return (
                comfy_audio,
                json.dumps(mix_info, indent=2),
                actual_duration,
                level_meters
            )
            
        except Exception as e:
            error_msg = f"Audio mixing error: {str(e)}"
            print(error_msg)
            
            # Return a minimal valid audio output to prevent crashes
            fallback_audio = torch.zeros(1, 2, int(44100 * output_duration), dtype=torch.float32)
            return (
                {"waveform": fallback_audio, "sample_rate": 44100},
                error_msg,
                0.0,
                json.dumps({"error": "Audio processing failed"})
            )
    
    def apply_smart_normalization(self, audio_data, mode, mix_info):
        """
        NEW: Intelligent normalization that preserves volume relationships
        """
        print(f"\n🔧 APPLYING NORMALIZATION MODE: {mode}")
        
        if mode == "off":
            print("   Normalization disabled - preserving exact levels")
            mix_info["processing_steps"].append("Normalization: OFF - exact levels preserved")
            return audio_data
        
        elif mode == "prevent_clipping":
            # Only reduce if clipping would occur, never boost
            max_val = torch.max(torch.abs(audio_data))
            if max_val > 0.99:
                scale_factor = 0.95 / max_val  # Leave small headroom
                normalized = audio_data * scale_factor
                print(f"   Prevented clipping: scaled by {scale_factor:.3f}")
                mix_info["processing_steps"].append(f"Clipping prevention: scaled by {scale_factor:.3f}")
                return normalized
            else:
                print(f"   No clipping risk (peak: {max_val:.3f}) - no changes made")
                mix_info["processing_steps"].append("Clipping prevention: no scaling needed")
                return audio_data
        
        elif mode == "full_normalize":
            # Traditional normalization - boost to maximum level
            max_val = torch.max(torch.abs(audio_data))
            if max_val > 0:
                target_level = 0.95
                scale_factor = target_level / max_val
                normalized = audio_data * scale_factor
                print(f"   Full normalization: scaled by {scale_factor:.3f}")
                mix_info["processing_steps"].append(f"Full normalization: scaled by {scale_factor:.3f}")
                return normalized
            return audio_data
        
        elif mode == "smart_normalize":
            # Smart mode - only normalize if the signal is very quiet
            rms_level = torch.sqrt(torch.mean(audio_data ** 2))
            peak_level = torch.max(torch.abs(audio_data))
            
            # If RMS is below -30dB, apply gentle boosting
            if rms_level < 0.03:  # About -30dB
                # Boost RMS to around -20dB
                target_rms = 0.1  # About -20dB
                scale_factor = target_rms / rms_level
                # But don't let peaks exceed 0.9
                max_scale = 0.9 / peak_level if peak_level > 0 else 1.0
                final_scale = min(scale_factor, max_scale)
                
                normalized = audio_data * final_scale
                print(f"   Smart normalization: boosted quiet signal by {final_scale:.3f}")
                mix_info["processing_steps"].append(f"Smart normalization: boosted by {final_scale:.3f}")
                return normalized
            else:
                print(f"   Smart normalization: signal loud enough (RMS: {rms_level:.3f}) - no changes")
                mix_info["processing_steps"].append("Smart normalization: no boost needed")
                return audio_data
        
        return audio_data
    
    def extract_audio_data(self, audio_input):
        """Extract audio data from various ComfyUI audio formats"""
        
        try:
            print(f"Processing audio input type: {type(audio_input)}")
            
            # Handle LazyAudioMap (ComfyUI's lazy loading)
            if 'LazyAudioMap' in str(type(audio_input)):
                print("Detected LazyAudioMap")
                
                # Try accessing as dictionary using items()
                try:
                    if hasattr(audio_input, 'items'):
                        items = dict(audio_input.items())
                        print(f"LazyAudioMap items extracted: {list(items.keys())}")
                        if 'waveform' in items and 'sample_rate' in items:
                            return {
                                "waveform": items['waveform'],
                                "sample_rate": items['sample_rate']
                            }
                except Exception as items_error:
                    print(f"Error accessing LazyAudioMap items: {items_error}")
                
                # Try direct attribute access
                try:
                    if hasattr(audio_input, 'waveform') and hasattr(audio_input, 'sample_rate'):
                        return {
                            "waveform": audio_input.waveform,
                            "sample_rate": audio_input.sample_rate
                        }
                except Exception as attr_error:
                    print(f"Error accessing LazyAudioMap attributes: {attr_error}")
            
            # Handle direct dictionary format
            elif isinstance(audio_input, dict):
                print("Found direct dictionary format")
                if 'waveform' in audio_input and 'sample_rate' in audio_input:
                    return audio_input
                else:
                    print(f"Dictionary missing required keys. Available: {list(audio_input.keys())}")
            
            # Handle direct tensor
            elif isinstance(audio_input, torch.Tensor):
                print("Found direct tensor format")
                return {"waveform": audio_input, "sample_rate": 44100}
            
            # Handle tuple/list format
            elif isinstance(audio_input, (tuple, list)) and len(audio_input) >= 2:
                print("Found tuple/list format")
                return {"waveform": audio_input[0], "sample_rate": audio_input[1]}
            
            else:
                print(f"Unknown audio format: {type(audio_input)}")
                return None
                
        except Exception as e:
            print(f"Error extracting audio data: {e}")
            return None

    def process_audio_track(self, audio_input, track_name, volume, start_time, 
                           fade_in, fade_out, target_sample_rate, output_duration):
        """Process individual audio track with all effects"""
        
        try:
            # Extract audio data using our robust method
            audio_dict = self.extract_audio_data(audio_input)
            if audio_dict is None:
                print(f"Failed to extract audio data from {track_name}")
                return None
            
            # Get waveform and sample rate
            if isinstance(audio_dict, dict):
                waveform = audio_dict.get("waveform")
                original_sample_rate = audio_dict.get("sample_rate", target_sample_rate)
            else:
                waveform = audio_dict
                original_sample_rate = target_sample_rate
            
            print(f"\n🎧 PROCESSING {track_name}:")
            print(f"   Original sample rate: {original_sample_rate}, Target: {target_sample_rate}")
            print(f"   Requested volume: {volume}")
            
            # Ensure tensor is on CPU for processing
            if isinstance(waveform, torch.Tensor):
                audio_data = waveform.cpu().float()
            else:
                audio_data = torch.tensor(waveform, dtype=torch.float32)
            
            print(f"   Input shape: {audio_data.shape}")
            
            # Handle tensor dimensions
            # ComfyUI audio format is typically [batch, channels, samples]
            if len(audio_data.shape) == 3:
                audio_data = audio_data[0]  # Remove batch dimension -> [channels, samples]
                print(f"   Removed batch dimension: {audio_data.shape}")
            elif len(audio_data.shape) == 1:
                audio_data = audio_data.unsqueeze(0)  # Add channel dimension -> [1, samples]
                print(f"   Added channel dimension: {audio_data.shape}")
            elif len(audio_data.shape) == 2:
                # Check if it's [samples, channels] and transpose if needed
                if audio_data.shape[0] > audio_data.shape[1]:
                    audio_data = audio_data.transpose(0, 1)  # -> [channels, samples]
                    print(f"   Transposed to [channels, samples]: {audio_data.shape}")
            
            # Convert to stereo if mono
            if audio_data.shape[0] == 1:
                audio_data = audio_data.repeat(2, 1)  # Duplicate mono to stereo
                print(f"   Converted mono to stereo: {audio_data.shape}")
            elif audio_data.shape[0] > 2:
                # If more than 2 channels, take first 2
                audio_data = audio_data[:2, :]
                print(f"   Reduced to stereo from {audio_data.shape[0]} channels")
            
            # Calculate original duration
            original_duration = audio_data.shape[1] / original_sample_rate
            print(f"   Original duration: {original_duration:.2f}s at {original_sample_rate}Hz")
            
            # Check levels before processing
            original_rms = torch.sqrt(torch.mean(audio_data ** 2))
            original_peak = torch.max(torch.abs(audio_data))
            print(f"   Original levels - RMS: {original_rms:.6f}, Peak: {original_peak:.6f}")
            
            # Resample if needed
            if abs(original_sample_rate - target_sample_rate) > 100:  # Allow small differences
                print(f"   Resampling from {original_sample_rate}Hz to {target_sample_rate}Hz")
                try:
                    # Use high-quality resampling
                    resampled = torchaudio.functional.resample(
                        audio_data, 
                        orig_freq=int(original_sample_rate), 
                        new_freq=int(target_sample_rate),
                        resampling_method="sinc_interp_hann"
                    )
                    print(f"   Resampled shape: {resampled.shape}")
                    audio_data = resampled
                except Exception as resample_error:
                    print(f"   High-quality resample failed: {resample_error}")
                    # Fallback: simple linear interpolation
                    ratio = target_sample_rate / original_sample_rate
                    new_length = int(audio_data.shape[1] * ratio)
                    audio_data = torch.nn.functional.interpolate(
                        audio_data.unsqueeze(0), size=new_length, mode='linear', align_corners=False
                    ).squeeze(0)
                    print(f"   Fallback resample shape: {audio_data.shape}")
            else:
                print(f"   No resampling needed")
            
            # Calculate new duration after resampling
            new_duration = audio_data.shape[1] / target_sample_rate
            print(f"   New duration: {new_duration:.2f}s at {target_sample_rate}Hz")
            
            # Apply volume adjustment
            print(f"   Applying volume: {volume}x")
            audio_data = audio_data * volume
            
            # Check levels after volume adjustment
            volume_rms = torch.sqrt(torch.mean(audio_data ** 2))
            volume_peak = torch.max(torch.abs(audio_data))
            print(f"   Post-volume levels - RMS: {volume_rms:.6f}, Peak: {volume_peak:.6f}")
            
            # Apply fade effects
            if fade_in > 0 or fade_out > 0:
                print(f"   Applying fades: in={fade_in}s, out={fade_out}s")
                audio_data = self.apply_fades(
                    audio_data, fade_in, fade_out, target_sample_rate
                )
            
            # Prepare for timeline placement
            processed_track = {
                "name": track_name,
                "audio": audio_data,
                "start_time": start_time,
                "duration": new_duration,
                "original_duration": original_duration,
                "original_sample_rate": original_sample_rate,
                "applied_volume": volume,
                "final_rms": float(torch.sqrt(torch.mean(audio_data ** 2))),
                "final_peak": float(torch.max(torch.abs(audio_data)))
            }
            
            print(f"✅ {track_name} processed successfully:")
            print(f"   Final shape: {audio_data.shape}")
            print(f"   Duration: {new_duration:.2f}s")
            print(f"   Applied volume: {volume}x")
            print(f"   Final RMS: {processed_track['final_rms']:.6f}")
            print(f"   Final Peak: {processed_track['final_peak']:.6f}")
            print(f"   Start time: {start_time}s")
            
            return processed_track
            
        except Exception as e:
            print(f"❌ Error processing {track_name}: {str(e)}")
            return None
    
    def apply_fades(self, audio_data, fade_in_duration, fade_out_duration, sample_rate):
        """Apply fade in and fade out effects"""
        
        audio_length = audio_data.shape[1]
        
        # Fade in
        if fade_in_duration > 0:
            fade_in_samples = int(fade_in_duration * sample_rate)
            fade_in_samples = min(fade_in_samples, audio_length // 2)
            
            if fade_in_samples > 0:
                fade_curve = torch.linspace(0, 1, fade_in_samples)
                audio_data[:, :fade_in_samples] *= fade_curve.unsqueeze(0)
        
        # Fade out
        if fade_out_duration > 0:
            fade_out_samples = int(fade_out_duration * sample_rate)
            fade_out_samples = min(fade_out_samples, audio_length // 2)
            
            if fade_out_samples > 0:
                fade_curve = torch.linspace(1, 0, fade_out_samples)
                audio_data[:, -fade_out_samples:] *= fade_curve.unsqueeze(0)
        
        return audio_data
    
    def mix_tracks(self, processed_tracks, output_duration, sample_rate):
        """Mix all processed tracks onto a timeline - preserving volume relationships!"""
        
        # Create output timeline [1, channels, samples]
        output_samples = int(output_duration * sample_rate)
        mixed_audio = torch.zeros(1, 2, output_samples, dtype=torch.float32)
        
        print(f"\n🎛️ MIXING TRACKS (Volume relationships preserved!):")
        print(f"Timeline: {output_duration}s ({output_samples} samples at {sample_rate}Hz)")
        
        for track in processed_tracks:
            track_name = track["name"]
            start_sample = int(track["start_time"] * sample_rate)
            track_audio = track["audio"]
            
            print(f"\n📊 Mixing {track_name}:")
            print(f"   Applied volume: {track['applied_volume']}x")
            print(f"   Final RMS: {track['final_rms']:.6f}")
            print(f"   Final Peak: {track['final_peak']:.6f}")
            print(f"   Start time: {track['start_time']}s (sample {start_sample})")
            print(f"   Track shape: {track_audio.shape}")
            print(f"   Track duration: {track['duration']:.2f}s")
            
            # Ensure track audio has correct dimensions
            if len(track_audio.shape) == 2:
                track_audio = track_audio.unsqueeze(0)  # Add batch dimension
                print(f"   Added batch dimension: {track_audio.shape}")
            
            # Calculate how much of the track fits in the output
            track_length = track_audio.shape[2]
            end_sample = start_sample + track_length
            
            print(f"   Track samples: {track_length}")
            print(f"   End sample: {end_sample}")
            
            # Clip to output bounds
            if start_sample < output_samples and end_sample > 0:
                # Calculate actual mixing range
                mix_start = max(0, start_sample)
                mix_end = min(output_samples, end_sample)
                
                # Calculate corresponding track range
                track_start = max(0, -start_sample)
                track_end = track_start + (mix_end - mix_start)
                
                print(f"   Mixing range: samples {mix_start}-{mix_end} (timeline)")
                print(f"   Track range: samples {track_start}-{track_end} (track)")
                print(f"   Mixing duration: {(mix_end - mix_start) / sample_rate:.2f}s")
                
                # Get the audio segment to mix
                audio_segment = track_audio[0, :, track_start:track_end]
                print(f"   Audio segment shape: {audio_segment.shape}")
                print(f"   Audio segment RMS: {torch.sqrt(torch.mean(audio_segment ** 2)):.6f}")
                
                # Mix the audio (ADDITIVE - preserves volume relationships!)
                mixed_audio[0, :, mix_start:mix_end] += audio_segment
                print(f"   ✅ Mixed into timeline (volumes preserved)")
            else:
                print(f"   ⚠️ Track outside timeline bounds - skipped")
        
        # Check final mixed audio levels
        final_rms = torch.sqrt(torch.mean(mixed_audio ** 2))
        final_peak = torch.max(torch.abs(mixed_audio))
        print(f"\n🎵 RAW MIX LEVELS (before master processing):")
        print(f"   Output shape: {mixed_audio.shape}")
        print(f"   RMS level: {final_rms:.6f}")
        print(f"   Peak level: {final_peak:.6f}")
        print(f"   Mix contains {len(processed_tracks)} tracks with preserved volume relationships")
        
        return mixed_audio
    
    def apply_compression(self, audio_data, ratio):
        """Apply dynamic range compression"""
        
        threshold = 0.7  # -3dB threshold
        
        # Calculate envelope
        envelope = torch.abs(audio_data)
        
        # Apply compression above threshold
        compressed = audio_data.clone()
        above_threshold = envelope > threshold
        
        if torch.any(above_threshold):
            # Compress the portion above threshold
            excess = envelope[above_threshold] - threshold
            compressed_excess = excess / ratio
            new_envelope = threshold + compressed_excess
            
            # Apply compression while preserving phase
            gain_reduction = new_envelope / envelope[above_threshold]
            compressed[above_threshold] *= gain_reduction
        
        return compressed
    
    def apply_limiter(self, audio_data, threshold_db):
        """Apply soft limiting to prevent clipping"""
        
        threshold_linear = 10 ** (threshold_db / 20)
        
        # Soft limiting using tanh
        limited = torch.tanh(audio_data / threshold_linear) * threshold_linear
        
        return limited
    
    def generate_level_meters(self, audio_data):
        """Generate level meter information for the mixed audio"""
        
        # Calculate RMS and peak levels for stereo
        audio_np = audio_data[0].numpy()  # Remove batch dimension
        
        rms_left = torch.sqrt(torch.mean(audio_data[0, 0] ** 2))
        rms_right = torch.sqrt(torch.mean(audio_data[0, 1] ** 2))
        peak_left = torch.max(torch.abs(audio_data[0, 0]))
        peak_right = torch.max(torch.abs(audio_data[0, 1]))
        
        # Convert to dB
        rms_left_db = 20 * torch.log10(rms_left + 1e-10)
        rms_right_db = 20 * torch.log10(rms_right + 1e-10)
        peak_left_db = 20 * torch.log10(peak_left + 1e-10)
        peak_right_db = 20 * torch.log10(peak_right + 1e-10)
        
        level_info = {
            "rms_left_db": float(rms_left_db),
            "rms_right_db": float(rms_right_db),
            "peak_left_db": float(peak_left_db),
            "peak_right_db": float(peak_right_db),
            "stereo_balance": "centered" if abs(rms_left_db - rms_right_db) < 3 else "unbalanced"
        }
        
        return json.dumps(level_info, indent=2)


# Node registration for ComfyUI
NODE_CLASS_MAPPINGS = {
    "GeekyAudioMixer": GeekyAudioMixer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GeekyAudioMixer": "🎵 Geeky AudioMixer (Fixed)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
