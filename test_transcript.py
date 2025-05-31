import streamlit as st
from transcript_extractor import extract_transcript

st.set_page_config(page_title="Transcript Extractor", layout="centered")
st.title("🎧 Extract Transcript from Uploaded Video")

video_path = st.text_input("Paste the video path you copied from upload step:")

if st.button("Extract Transcript"):
    if video_path:
        st.info("Transcribing with OpenAI Whisper...")
        transcript = extract_transcript(video_path)
        if transcript:
            st.success("✅ Transcript:")
            st.write(transcript)
    else:
        st.warning("⚠️ Please paste a valid file path.")
