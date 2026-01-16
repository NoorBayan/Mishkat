import subprocess
import os

def merge_videos_with_transition(
    video1: str,
    video2: str,
    output_video: str,
    transition_duration: float = 1.2
):
    """
    Merge two videos with visual transition ONLY (no audio overlap).
    Audio plays sequentially.
    """

    import subprocess
    import os

    if not os.path.exists(video1):
        raise FileNotFoundError(f"❌ Missing video: {video1}")
    if not os.path.exists(video2):
        raise FileNotFoundError(f"❌ Missing video: {video2}")

    # Duration of first video
    probe_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video1
    ]

    duration_v1 = float(
        subprocess.check_output(probe_cmd).decode().strip()
    )

    offset = max(0, duration_v1 - transition_duration)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", video1,
        "-i", video2,
        "-filter_complex",
        (
            f"[0:v][1:v]xfade=transition=fade:"
            f"duration={transition_duration}:offset={offset}[v];"
            f"[0:a][1:a]concat=n=2:v=0:a=1[a]"
        ),
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_video
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("❌ Video merge failed")

    print(f"✅ Final video created: {output_video}")
