import openai
import streamlit as st

openai.api_key = st.secrets["openai_api_key"]


def fake_voice_analysis(video_path):
    try:
        # Get transcript with word-level timestamps
        with open(video_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        
        words = result.words
        total_words = len(words)
        duration = result.duration
        wpm = round((total_words / duration) * 60, 2) if duration > 0 else 0

        return {
            "speech_speed_wpm": wpm,
            "music_background": "Unknown",  # Placeholder
            "volume_range": "Unknown"       # Placeholder
        }

    except Exception as e:
        raise RuntimeError(f"Voice analysis failed: {e}")
