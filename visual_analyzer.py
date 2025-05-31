# Step 2: Visual Analysis
st.subheader("🎬 Visual Analysis")

# Duration via OpenCV
cap = cv2.VideoCapture(temp_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
duration = round(frame_count / fps, 2) if fps > 0 else 0

# Brightness and cuts
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
