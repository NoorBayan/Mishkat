import streamlit as st

from src.data.loaders import (
    load_ayahs,
    load_translations,
    load_reciters
)

from src.data.accessors import (
    get_ayah_text,
    get_translation_data
)

from src.config.chapters import CHAPTERS_AR, CHAPTERS_EN
from src.config.ayah_counts import AYAH_COUNTS
from src.config.translations import LANGUAGE_MAP, TRANSLATION_MAP
from src.config.frames import QURAN_FRAME_TEMPLATES

from src.pipeline.create_ayah_video import create_ayah_video
