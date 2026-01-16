import os
import requests

# Internal module imports
from ..utils.io import download_audio_from_gdrive
from ..slide.renderer import render_quran_slide_from_template, pptx_to_png
from ..video.image import image_and_audio_to_video
from ..video.merge import merge_videos_with_transition
from ..video.display import display_video_html

def create_ayah_video(
    surah_name,
    surah_name_en,
    verse_number,
    ayah_text,
    translation_text,
    audio_url,
    file_id,
    frame_template
):
    """
    High-level pipeline to generate a final Ayah video:
    Arabic → Translation → Transition → Final MP4
    """

    # -------------------------------------------------
    # 0) Paths & constants
    # -------------------------------------------------
    BASE_TEMPLATE_DIR = "/content/Mishkat/templates"
    TEMPLATE_PATH = os.path.join(BASE_TEMPLATE_DIR, f"{frame_template}.pptx")


    TMP_PPTX_DIR = "/content/tmp_pptx"
    IMG_DIR = "/content/output_images"
    VIDEO_DIR = "/content/output_videos"
    AUDIO_DIR = "/content/audio"

    os.makedirs(TMP_PPTX_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # -------------------------------------------------
    # 1) Download audios
    # -------------------------------------------------
    arabic_audio_path = f"{AUDIO_DIR}/{verse_number}_ar.mp3"
    translation_audio_path = f"{AUDIO_DIR}/{verse_number}_tr.wav"

    # Arabic audio (direct URL)
    r = requests.get(audio_url)
    with open(arabic_audio_path, "wb") as f:
        f.write(r.content)

    # Translation audio (Google Drive)
    translation_audio_path = download_audio_from_gdrive(
        gdrive_url=f"https://drive.google.com/file/d/{file_id}/view",
        output_path=translation_audio_path
    )

    # -------------------------------------------------
    # 2) Arabic slide → image → video
    # -------------------------------------------------
    arabic_pptx = f"{TMP_PPTX_DIR}/ayah_{verse_number}_ar.pptx"
    arabic_video = f"{VIDEO_DIR}/ayah_{verse_number}_ar.mp4"

    render_quran_slide_from_template(
        template_pptx=TEMPLATE_PATH,
        output_pptx=arabic_pptx,
        ayah_number=verse_number,
        surah_name=surah_name,
        ayah_text=ayah_text
    )

    pptx_to_png(arabic_pptx, IMG_DIR)

    arabic_image = f"{IMG_DIR}/{os.path.splitext(os.path.basename(arabic_pptx))[0]}.png"

    image_and_audio_to_video(
        image_path=arabic_image,
        audio_path=arabic_audio_path,
        output_video=arabic_video
    )

    # -------------------------------------------------
    # 3) Translation slide → image → video
    # -------------------------------------------------
    translation_pptx = f"{TMP_PPTX_DIR}/ayah_{verse_number}_tr.pptx"
    translation_video = f"{VIDEO_DIR}/ayah_{verse_number}_tr.mp4"

    render_quran_slide_from_template(
        template_pptx=TEMPLATE_PATH,
        output_pptx=translation_pptx,
        ayah_number=verse_number,
        surah_name=surah_name_en,
        ayah_text=translation_text
    )

    pptx_to_png(translation_pptx, IMG_DIR)

    translation_image = f"{IMG_DIR}/{os.path.splitext(os.path.basename(translation_pptx))[0]}.png"

    image_and_audio_to_video(
        image_path=translation_image,
        audio_path=translation_audio_path,
        output_video=translation_video
    )

    # -------------------------------------------------
    # 4) Merge videos with transition
    # -------------------------------------------------
    final_video = f"{VIDEO_DIR}/ayah_{verse_number}_final.mp4"

    merge_videos_with_transition(
        video1=arabic_video,
        video2=translation_video,
        output_video=final_video,
        transition_duration=1.2
    )

    display_video_html(final_video)

    # -------------------------------------------------
    # 5) Done
    # -------------------------------------------------
    print("🎉 Ayah video created successfully")
    return final_video
