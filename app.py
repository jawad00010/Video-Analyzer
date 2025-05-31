import streamlit as st
import tempfile
from openai import OpenAI
import numpy as np
import cv2
from voice_analyzer import extract_audio_features


# Load OpenAI API Key
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="AI Video Ad Analyzer", layout="centered")
st.title("📊 AI Video Ad Performance Predictor")

# Upload section
uploaded_file = st.file_uploader("Upload your ad video (.mp4)", type=["mp4"])
market = st.selectbox("Target Market", ["UAE", "KSA", "Qatar", "Kuwait", "Global"])

if uploaded_file:
    # Save video
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_file.read())
    temp_video_path = temp_video.name

    st.video(uploaded_file)
    st.success("✅ Video uploaded and saved temporarily.")
    st.session_state["video_path"] = temp_video_path
    st.session_state["market"] = market

    if st.button("Extract & Analyze"):
        try:
            # Step 1: Transcript (Whisper)
            with open(temp_video_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            transcript_text = transcript.text
            st.subheader("📜 Transcript")
            st.write(transcript_text)

            # Step 2: Visual Analysis
            st.subheader("🎬 Visual Analysis")
    # duration 
            cap = cv2.VideoCapture(temp_video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = round(frame_count / fps, 2) if fps > 0 else 0

            # Brightness and cuts using OpenCV
            cap = cv2.VideoCapture(temp_video_path)
            frame_count = 0
            brightness_total = 0
            cuts = 0
            _, prev = cap.read()
            i = 0

            while True:
                ret, curr = cap.read()
                if not ret:
                    break
                gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
                brightness_total += np.mean(gray)
                frame_count += 1

                if i % 20 == 0 and prev is not None:
                    diff = cv2.absdiff(cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY), gray)
                    score = np.sum(diff) / diff.size
                    if score > 30:
                        cuts += 1
                    prev = curr
                i += 1
            cap.release()

            avg_brightness = round(brightness_total / frame_count, 2) if frame_count else 0
            avg_scene_length = round(duration / cuts, 2) if cuts > 0 else duration

            st.write(f"⏱️ Duration: {duration} seconds")
            st.write(f"💡 Average Brightness: {avg_brightness}")
            st.write(f"✂️ Scene Cuts: {cuts}")
            st.write(f"🕒 Avg Scene Length: {avg_scene_length} seconds")
        
            # Step 3: Voiceover Analysis
            st.subheader("🔊 Voiceover Analysis")
            voice_features = extract_audio_features(temp_video_path)
            
            st.write(f"🗣️ Speaking Speed: {voice_features['speech_speed_wpm']} WPM")
            st.write(f"🎵 Background Music: {voice_features['music_background']}")
            st.write(f"🔊 Volume Range: {voice_features['volume_range']}")

            # Step 3: GPT Evaluation
            st.subheader("🤖 GPT Performance Evaluation")

            prompt = f"""
            You are a video ad performance analyst for TikTok and Meta platforms.

            Analyze the following video for its potential success in the {market} market.

            Transcript:
            \"\"\"{transcript_text}\"\"\"

            Visual Info:
            - Duration: {duration} seconds
            - Brightness: {avg_brightness}
            - Scene Cuts: {cuts}
            - Avg Scene Length: {avg_scene_length} seconds

            Please provide:
            1. Estimated probability of success (0–100%)
            2. Short reason
            3. 2 suggestions to improve performance
            4. Type of hook/tone/style
            """

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content
            st.markdown("### 🧠 GPT Response:")
            st.write(result)

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
