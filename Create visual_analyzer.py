# visual_analyzer.py

import cv2
import numpy as np
from moviepy.editor import VideoFileClip

def analyze_visuals(video_path):
    # Load video
    clip = VideoFileClip(video_path)
    duration = round(clip.duration, 2)  # seconds

    # OpenCV brightness analysis
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    brightness_total = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness_total += np.mean(gray)
        frame_count += 1

    cap.release()

    avg_brightness = round(brightness_total / frame_count, 2) if frame_count else 0

    # Basic scene cut approximation: sample every 20th frame
    cap = cv2.VideoCapture(video_path)
    scene_changes = 0
    _, prev = cap.read()
    i = 0

    while True:
        ret, curr = cap.read()
        if not ret:
            break
        if i % 20 == 0:
            diff = cv2.absdiff(cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY), cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY))
            score = np.sum(diff) / diff.size
            if score > 30:  # threshold for scene change
                scene_changes += 1
            prev = curr
        i += 1

    cap.release()

    cuts = scene_changes
    avg_scene_length = round(duration / cuts, 2) if cuts > 0 else duration

    return {
        "duration": duration,
        "avg_brightness": avg_brightness,
        "scene_cuts": cuts,
        "scene_pace": avg_scene_length
    }
