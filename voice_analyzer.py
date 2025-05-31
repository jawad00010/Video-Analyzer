from moviepy.editor import VideoFileClip
import librosa
import numpy as np
import tempfile

def extract_audio_features(video_path):
    # Extract audio using moviepy
    audio_clip = VideoFileClip(video_path).audio
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    audio_clip.write_audiofile(temp_wav, codec='pcm_s16le', verbose=False, logger=None)

    # Load using librosa
    y, sr = librosa.load(temp_wav)

    # Speaking Speed Estimation (based on energy bursts)
    frames = librosa.util.frame(y, frame_length=2048, hop_length=512)
    energy = np.sum(frames**2, axis=0)
    speech_frames = energy > np.percentile(energy, 85)
    speech_ratio = np.sum(speech_frames) / len(speech_frames)
    speech_speed = round(speech_ratio * 180, 2)  # Estimated WPM

    # Volume range detection
    rms = librosa.feature.rms(y=y).flatten()
    volume_range = round(np.max(rms) - np.min(rms), 4)
    music_detected = volume_range > 0.02

    return {
        "speech_speed_wpm": speech_speed,
        "music_background": "Yes" if music_detected else "No",
        "volume_range": volume_range
    }
