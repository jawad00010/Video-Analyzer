# transcript_extractor.py

from openai import OpenAI
import streamlit as st

# Get the OpenAI key securely from secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

def extract_transcript(video_path):
    try:
        with open(video_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        st.error(f"❌ Transcript extraction failed: {e}")
        return None
