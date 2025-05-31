from pydub import AudioSegment
import librosa
import numpy as np
import tempfile

def extract_audio_features(video_path):
    # Convert MP4 to WAV
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    audio = AudioSegment.from_file(video_path)
    audio.export(temp_wav, format="wav")

    # Load using librosa
    y, sr = librosa.load(temp_wav)

    # Speaking Speed Estimation (based on energy bursts)
    frames = librosa.util.frame(y, frame_length=2048, hop_length=512)
    energy = np.sum(frames**2, axis=0)
    speech_frames = energy > np.percentile(energy, 85)
    speech_ratio = np.sum(speech_frames) / len(speech_frames)
    speech_speed = round(speech_ratio * 180, 2)  # Est. words per minute

    # Volume range detection
    rms = librosa.feature.rms(y=y).flatten()
    volume_range = round(np.max(rms) - np.min(rms), 4)

    # Classification
    music_detected = volume_range > 0.02

    return {
        "speech_speed_wpm": speech_speed,
        "music_background": "Yes" if music_detected else "No",
        "volume_range": volume_range
    }
