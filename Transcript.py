# transcript_extractor.py

import openai
import streamlit as st

# Load API key securely (already in Streamlit secrets)
openai.api_key = st.secrets["openai_api_key"]

def extract_transcript(audio_path):
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]
    except Exception as e:
        st.error(f"Transcript extraction failed: {e}")
        return None
