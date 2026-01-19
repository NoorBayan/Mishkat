import os
import base64
from IPython.display import HTML, display

def display_video_html(video_path, width=640, height=480):
    if not isinstance(video_path, str):
        raise TypeError(f"video_path must be str, got {type(video_path)}")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"❌ Video not found: {video_path}")

    with open(video_path, "rb") as f:
        video_base64 = base64.b64encode(f.read()).decode("utf-8")

    video_html = f"""
    <video width="{width}" height="{height}" controls>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    """

    display(HTML(video_html))
