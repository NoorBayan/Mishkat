import os
import subprocess
from tqdm import tqdm

def image_and_audio_to_video(
    image_path: str,
    audio_path: str,
    output_video: str
):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"❌ Image not found: {image_path}")

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"❌ Audio not found: {audio_path}")

    os.makedirs(os.path.dirname(output_video), exist_ok=True)

    # استخراج مدة الصوت
    probe_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]

    duration = float(subprocess.check_output(probe_cmd).decode().strip())

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-progress", "pipe:1",
        "-nostats",
        output_video
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    pbar = tqdm(total=duration, unit="sec", desc="🎬 Rendering video")

    for line in process.stdout:
        if "out_time_ms=" in line:
            ms = int(line.strip().split("=")[1])
            pbar.n = ms / 1_000_000
            pbar.refresh()

    process.wait()
    pbar.close()

    if process.returncode != 0:
        raise RuntimeError("❌ ffmpeg failed")

    print(f"✅ Video created: {output_video}")
