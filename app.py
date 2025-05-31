import streamlit as st
import tempfile
from openai import OpenAI

# Load OpenAI key from Streamlit Secrets
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="Video Transcript Extractor", layout="centered")
st.title("🎥 Upload Ad Video & Extract Transcript")

# Step 1: Upload
uploaded_file = st.file_uploader("Upload a video (.mp4)", type=["mp4"])
market = st.selectbox("Select Target Market", ["UAE", "KSA", "Qatar", "Kuwait", "Global"])

if uploaded_file:
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_file.read())
    temp_video_path = temp_video.name

    st.video(uploaded_file)
    st.success("✅ Video uploaded successfully!")

    st.session_state["video_path"] = temp_video_path
    st.session_state["market"] = market

    if st.button("Extract Transcript"):
        try:
            with open(temp_video_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            st.success("🎧 Transcript:")
            st.write(transcript.text)
        except Exception as e:
            st.error(f"❌ Transcript extraction failed: {e}")
from visual_analyzer import analyze_visuals

st.subheader("🎬 Visual Analysis")

visuals = analyze_visuals(temp_video_path)
st.write(f"📏 Duration: {visuals['duration']} sec")
st.write(f"🌕 Avg Brightness: {visuals['avg_brightness']}")
st.write(f"✂️ Scene Cuts Detected: {visuals['scene_cuts']}")
st.write(f"⏱️ Avg Scene Length: {visuals['scene_pace']} sec")

