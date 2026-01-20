import pandas as pd
import rarfile
from pathlib import Path

# المسار الحقيقي لمجلد data/csv
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "csv"


def load_ayahs():
    return pd.read_csv(
        DATA_DIR / "quran_verses.csv",
        sep="\t",
        encoding="utf-16"
    )


def load_reciters():
    return pd.read_csv(
        DATA_DIR / "reciters.csv",
        sep="\t",
        encoding="utf-16"
    )


def load_translations():
    rar_path = DATA_DIR / "quran_translations.rar"
    extract_dir = Path("/tmp/quran_translations")

    if not extract_dir.exists():
        extract_dir.mkdir(parents=True, exist_ok=True)
        with rarfile.RarFile(rar_path) as rf:
            rf.extractall(extract_dir)

    return pd.read_csv(
        extract_dir / "quran_translations.csv",
        sep="\t",
        encoding="utf-16"
    )
