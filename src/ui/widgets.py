# src/ui/widgets.py

import ipywidgets as widgets
from IPython.display import display

from Mishkat.src.config.chapters import CHAPTERS_AR, CHAPTERS_EN
from Mishkat.src.config.ayah_counts import AYAH_COUNTS
from Mishkat.src.config.translations import LANGUAGE_MAP, TRANSLATION_MAP
from Mishkat.src.config.frames import QURAN_FRAME_TEMPLATES

from Mishkat.src.data.loaders import (
    load_ayahs,
    load_translations,
    load_reciters
)

from Mishkat.src.data.accessors import (
    get_ayah_text,
    get_translation_data
)

from src.pipeline import create_ayah_video


# ============================================================
# Load data ONCE
# ============================================================

df_ayahs = load_ayahs()
df_translations = load_translations()
df_reciters = load_reciters()


# ============================================================
# Widgets
# ============================================================

surah_dropdown = widgets.Dropdown(
    options=[(name, num) for num, name in CHAPTERS_AR.items()],
    description="Surah:"
)

ayah_dropdown = widgets.Dropdown(description="Ayah:")

reciter_dropdown = widgets.Dropdown(
    options=[(row["name"], row["id"]) for _, row in df_reciters.iterrows()],
    description="Reciter:"
)

frame_dropdown = widgets.Dropdown(
    options=[(title, key) for key, title in QURAN_FRAME_TEMPLATES.items()],
    description="Frame:"
)

language_dropdown = widgets.Dropdown(
    options=[(name, code) for code, name in LANGUAGE_MAP.items()],
    description="Language:"
)

translator_dropdown = widgets.Dropdown(description="Translator:")

run_button = widgets.Button(
    description="🎬 Create Video",
    button_style="success"
)

output = widgets.Output()


# ============================================================
# Logic
# ============================================================

def update_ayahs(change):
    surah = change["new"]
    ayah_dropdown.options = list(range(1, AYAH_COUNTS[surah] + 1))
    ayah_dropdown.value = 1


def update_translators(change):
    lang = change["new"]
    translators = TRANSLATION_MAP.get(lang, [])
    translator_dropdown.options = translators
    translator_dropdown.value = translators[0] if translators else None


def on_run_clicked(_):

    output.clear_output()

    chapter_id = surah_dropdown.value
    verse_id = ayah_dropdown.value
    translator = translator_dropdown.value

    ayah_text = get_ayah_text(df_ayahs, chapter_id, verse_id)
    translation_text, file_id = get_translation_data(
        df_translations, chapter_id, verse_id, translator
    )

    if ayah_text is None or translation_text is None:
        with output:
            print("❌ Ayah or translation not found")
        return

    reciter_id = reciter_dropdown.value
    base_url = df_reciters.loc[
        df_reciters.id == reciter_id, "base_url"
    ].values[0]

    audio_url = f"{base_url}{chapter_id:03d}{verse_id:03d}.mp3"

    final_video = create_ayah_video(
        surah_name=CHAPTERS_AR[chapter_id],
        surah_name_en=CHAPTERS_EN[chapter_id],
        verse_number=verse_id,
        ayah_text=ayah_text,
        translation_text=translation_text,
        audio_url=audio_url,
        file_id=file_id,
        frame_template=frame_dropdown.value
    )

    with output:
        print("✅ Video created:", final_video)


# ============================================================
# Events
# ============================================================

surah_dropdown.observe(update_ayahs, names="value")
language_dropdown.observe(update_translators, names="value")
run_button.on_click(on_run_clicked)


# ============================================================
# Public API (THIS is what Colab calls)
# ============================================================

def launch_ui():
    surah_dropdown.value = 1
    update_ayahs({"new": 1})
    language_dropdown.value = "en"

    display(widgets.VBox([
        surah_dropdown,
        ayah_dropdown,
        reciter_dropdown,
        frame_dropdown,
        language_dropdown,
        translator_dropdown,
        run_button,
        output
    ]))

