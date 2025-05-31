import openai
import streamlit as st
from pydub import AudioSegment
import tempfile
import os

openai.api_key = st.secrets["openai_api_key"]

def fake_voice_analysis(video_path):
    try:
        # Extract first 30 seconds audio using pydub (no ffmpeg)
        audio = AudioSegment.from_file(video_path)
        short_audio = audio[:30_000]  # First 30 seconds

        # Export as low-bitrate MP3 under 1MB
        temp_mp3 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        short_audio.export(temp_mp3, format="mp3", bitrate="64k")

        with open(temp_mp3, "rb") as f:
            result = openai.Audio.transcribe(
                model="whisper-1",
                file=f,
                response_format="verbose_json"
            )

        words = result.get("words", [])
        total_words = len(words)
        duration = result.get("duration", 30)
        wpm = round((total_words / duration) * 60, 2) if duration > 0 else 0

        return {
            "speech_speed_wpm": wpm,
            "music_background": "Unknown",
            "volume_range": "Unknown"
        }

    except Exception as e:
        raise RuntimeError(f"Voice analysis failed: {e}")
