def get_ayah_text(df_ayahs, chapter_id, verse_id):
    row = df_ayahs[
        (df_ayahs.chapter_id == chapter_id) &
        (df_ayahs.verse_id == verse_id)
    ]
    return row.iloc[0]["verses"] if not row.empty else None


def get_translation_data(df_trans, chapter_id, verse_id, translator):
    row = df_trans[
        (df_trans.chapter_id == chapter_id) &
        (df_trans.verse_id == verse_id) &
        (df_trans.translation == translator)
    ]
    if row.empty:
        return None, None
    return row.iloc[0]["text"], row.iloc[0]["file_id"]
