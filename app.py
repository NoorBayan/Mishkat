# =====================================
# 0) FIX PYTHON PATH FOR STREAMLIT
# =====================================
import sys
import os

# Root of the project (folder containing app.py)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to src folder
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Add src to sys.path if not already there
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# =====================================
# 1) IMPORTS
# =====================================
import streamlit as st
import pandas as pd

# Import pipeline
from pipeline.create_ayah_video import create_ayah_video

# Import configs
from config.chapters import CHAPTERS_AR, CHAPTERS_EN
from config.ayah_counts import AYAH_COUNTS
from config.frames import QURAN_FRAME_TEMPLATES
from config.translations import LANGUAGE_MAP, TRANSLATION_MAP

# Import data loaders
from data.loaders import load_ayahs, load_translations, load_reciters

# Import data accessors
from data.accessors import get_ayah_text, get_translation_data

# =====================================
# 2) APP CONFIG (العنوان)
# =====================================
st.set_page_config(
    page_title="Mishkat – Quran Ayah Generator",
    layout="centered"
)

st.title("📖 Mishkat – Quran Ayah Video Generator")

# =====================================
# 3) LOAD DATA (مرة واحدة فقط)
# =====================================
@st.cache_data
def load_all_data():
    return (
        load_ayahs(),
        load_translations(),
        load_reciters()
    )

df_ayahs, df_translations, reciters_df = load_all_data()

# =====================================
# 4) UI CONTROLS (القوائم)
# =====================================
surah_id = st.selectbox(
    "Surah",
    options=list(CHAPTERS_AR.keys()),
    format_func=lambda x: CHAPTERS_AR[x]
)

ayah_id = st.selectbox(
    "Ayah",
    options=list(range(1, AYAH_COUNTS[surah_id] + 1))
)

reciter_id = st.selectbox(
    "Reciter",
    options=reciters_df["id"].tolist(),
    format_func=lambda x: reciters_df.loc[
        reciters_df.id == x, "name"
    ].values[0]
)

frame_template = st.selectbox(
    "Visual Frame",
    options=list(QURAN_FRAME_TEMPLATES.keys()),
    format_func=lambda x: QURAN_FRAME_TEMPLATES[x]
)

language = st.selectbox(
    "Translation Language",
    options=list(LANGUAGE_MAP.keys()),
    format_func=lambda x: LANGUAGE_MAP[x]
)

translator = st.selectbox(
    "Translator",
    options=TRANSLATION_MAP[language]
)

# =====================================
# 5) EXECUTION BUTTON
# =====================================
if st.button("🎬 Generate Ayah Video"):

    ayah_text = get_ayah_text(df_ayahs, surah_id, ayah_id)
    translation_text, file_id = get_translation_data(
        df_translations,
        surah_id,
        ayah_id,
        translator
    )

    if not ayah_text or not translation_text:
        st.error("Ayah or translation not found")
        st.stop()

    with st.spinner("Rendering video..."):

        final_video = create_ayah_video(
            surah_name=CHAPTERS_AR[surah_id],
            surah_name_en=CHAPTERS_EN[surah_id],
            verse_number=ayah_id,
            ayah_text=ayah_text,
            translation_text=translation_text,
            audio_url=None,
            file_id=file_id,
            frame_template=frame_template
        )

    st.success("Video created successfully!")
    st.video(final_video)
