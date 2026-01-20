import pandas as pd
import rarfile
import os

BASE_DATA = "data/csv"

def load_ayahs():
    return pd.read_csv(
        f"{BASE_DATA}/quran_verses.csv",
        sep="\t",
        encoding="utf-16"
    )

def load_reciters():
    return pd.read_csv(
        f"{BASE_DATA}/reciters.csv",
        sep="\t",
        encoding="utf-16"
    )

def load_translations():
    rar_path = f"{BASE_DATA}/quran_translations.rar"
    extract_dir = "/tmp/quran_translations"

    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)
        with rarfile.RarFile(rar_path) as rf:
            rf.extractall(extract_dir)

    return pd.read_csv(
        f"{extract_dir}/quran_translations.csv",
        sep="\t",
        encoding="utf-16"
    )
