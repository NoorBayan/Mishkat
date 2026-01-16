# src/video/display.py

import os

def display_video_html(video_path: str):
    """
    Placeholder for notebook environments.
    In Streamlit, video display is handled via st.video().
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"❌ Video not found: {video_path}")

    return video_path
