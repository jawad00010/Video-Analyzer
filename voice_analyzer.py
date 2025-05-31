import openai
from moviepy.editor import VideoFileClip
import tempfile
import os

def analyze_voice(video_path):
    try:
        # Extract audio from first 30s
        clip = VideoFileClip(video_path).subclip(0, 30)
        temp_audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        clip.audio.write_audiofile(temp_audio_path, bitrate="64k")

        # Send to Whisper API
        with open(temp_audio_path, "rb") as audio_file:
            result = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )

        words = result.get("words", [])
        total_words = len(words)
        duration = result.get("duration", 30)
        wpm = round((total_words / duration) * 60, 2) if duration > 0 else 0

        return {
            "speech_speed_wpm": wpm,
            "voice_summary": "Clear and moderately paced" if wpm > 110 else "Slow delivery",
        }

    except Exception as e:
        return {"error": f"❌ Voice analysis failed: {e}"}
