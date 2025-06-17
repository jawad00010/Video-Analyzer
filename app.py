import streamlit as st
import tempfile
import cv2
import numpy as np
from openai import OpenAI
from training_loader import load_training_examples

# Set Streamlit config (must be first)
st.set_page_config(page_title="AI Video Ad Analyzer", layout="centered")
st.title("🎥 Ad Performance Video Analyzer")

# Load OpenAI client
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Upload video
uploaded_file = st.file_uploader("Upload your ad video (.mp4, .mov, .mkv)", type=["mp4", "mov", "mkv"])
market = st.selectbox("Target Market", ["UAE", "KSA", "Qatar", "Kuwait", "Global"])

if uploaded_file:
    # Save video temporarily
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_file.read())
    temp_video_path = temp_video.name

    st.video(uploaded_file)
    st.success("✅ Video uploaded successfully.")

    if st.button("Extract & Analyze"):
        try:
            # Step 1: Transcript (Whisper)
            from moviepy.editor import VideoFileClip

# Step 1: Extract Audio and Get Transcript
st.subheader("📜 Transcript")

        # Extract audio from video and save as temporary mp3
        audio_path = temp_video_path.replace(".mp4", ".mp3")
        video_clip = VideoFileClip(temp_video_path)
        video_clip.audio.write_audiofile(audio_path)
        
        # Transcribe using Whisper
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

transcript_text = transcript.text
st.write(transcript_text)

            transcript_text = transcript.text
            st.subheader("📜 Transcript")
            st.write(transcript_text)

            # Step 2: Visual Analysis
            st.subheader("🎬 Visual Analysis")

            cap = cv2.VideoCapture(temp_video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = round(total_frames / fps, 2) if fps > 0 else 0

            brightness_total = 0
            cuts = 0
            frame_count = 0
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
            st.write(f"💡 Avg Brightness: {avg_brightness}")
            st.write(f"✂️ Scene Cuts: {cuts}")
            st.write(f"🕒 Avg Scene Length: {avg_scene_length} seconds")

            # Step 3: GPT Performance Evaluation
            st.subheader("🤖 GPT Performance Evaluation")

            examples = load_training_examples()

            prompt = "You are a video ad performance analyst for TikTok and Meta platforms.\n\n"

            for i, ex in enumerate(examples):
                prompt += f"""
Example {i+1}:
Transcript: {ex['transcript'][:500]}...
Visuals:
- Duration: {ex['duration']}s
- Brightness: {ex['brightness']}
- Scene Cuts: {ex['cuts']}
- Avg Scene Length: {ex['avg_scene_length']}s
Market: {ex['market']}
Performance: {ex['label']}

"""

            prompt += f"""
Now evaluate this new ad in the {market} market:

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

            gpt_result = response.choices[0].message.content.strip()
            st.markdown("### 🧠 GPT Response:")
            st.write(gpt_result)

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")
