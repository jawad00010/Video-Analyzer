import ffmpeg
import librosa
import numpy as np
import tempfile
import os

def extract_audio_features(video_path):
    # Step 1: Extract audio from video using ffmpeg-python
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

    ffmpeg.input(video_path).output(temp_wav, format='wav', acodec='pcm_s16le', ac=1, ar='16k').run(quiet=True, overwrite_output=True)

    # Step 2: Load with librosa
    y, sr = librosa.load(temp_wav)

    # Step 3: Voice speed estimation
    frames = librosa.util.frame(y, frame_length=2048, hop_length=512)
    energy = np.sum(frames**2, axis=0)
    speech_frames = energy > np.percentile(energy, 85)
    speech_ratio = np.sum(speech_frames) / len(speech_frames)
    speech_speed = round(speech_ratio * 180, 2)

    # Step 4: Volume & music detection
    rms = librosa.feature.rms(y=y).flatten()
    volume_range = round(np.max(rms) - np.min(rms), 4)
    music_detected = volume_range > 0.02

    # Clean up
    os.remove(temp_wav)

    return {
        "speech_speed_wpm": speech_speed,
        "music_background": "Yes" if music_detected else "No",
        "volume_range": volume_range
    }
