import streamlit as st
import tempfile

# Streamlit page config
st.set_page_config(page_title="Ad Video Upload", layout="centered")
st.title("🎥 Upload Your Ad Video")

# Step 1: Upload video file
uploaded_file = st.file_uploader("Upload a video (.mp4)", type=["mp4"])

# Step 2: Select the target market
market = st.selectbox("Select Target Market", ["UAE", "KSA", "Qatar", "Kuwait", "Global"])

# Step 3: Save and display video if uploaded
if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video.write(uploaded_file.read())
    temp_video_path = temp_video.name

    # Display video in app
    st.video(uploaded_file)
    st.success(f"✅ Video uploaded successfully!\n\nSaved to: `{temp_video_path}`")
    st.write(f"🎯 Selected Market: **{market}**")

    # Optionally return or store for next module
    st.session_state["video_path"] = temp_video_path
    st.session_state["market"] = market
