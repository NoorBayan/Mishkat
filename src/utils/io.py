import os
import re
import requests

def download_audio_from_gdrive(gdrive_url: str, output_path: str):
    """
    Downloads a file from Google Drive (public link) to a local path.
    """

    # Extract file ID
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", gdrive_url)
    if not match:
        raise ValueError("❌ Invalid Google Drive URL")

    file_id = match.group(1)
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(download_url, stream=True)
    response.raise_for_status()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"✅ Audio downloaded: {output_path}")
    return output_path
