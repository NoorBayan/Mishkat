# 🕌 Mishkat

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)
[![Status](https://img.shields.io/badge/Status-Active_Research-orange.svg)]()

> **Mishkat** is an advanced content automation engine designed to generate professional Quranic videos programmatically. It bridges structured data with visual design by rendering dynamic PowerPoint templates into high-definition video sequences using FFmpeg.

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔭 Overview

Mishkat was built to solve the scalability issue in producing high-quality educational Quranic content. Instead of manually editing video frames, Mishkat treats video production as a **code-first pipeline**.

It utilizes a headless implementation of **LibreOffice** for high-fidelity rendering of `.pptx` slides and **FFmpeg** for complex media merging, allowing for the generation of thousands of verses in varying templates and languages with a single command.

---

## ✨ Key Features

*   **⚡ Automated Pipeline:** Transform CSV data (Ayahs, Translations) into MP4 videos instantly.
*   **🎨 Template-Driven Design:** Decouples logic from design. Designers work in PowerPoint (`.pptx`), and the engine populates content dynamically.
*   **📐 Smart Layout Algorithm:** Features a custom heuristic (`estimate_font_size`) to dynamically adjust font sizes based on text density and bounding box constraints.
*   **🌍 Multi-Language Support:** Native handling for Bi-directional text (RTL for Arabic/Urdu, LTR for English/Latin) with correct shaping.
*   **🎬 Professional Rendering:** Seamless stitching of audio and visual assets with automated cross-fade transitions.

---

## 🏗 System Architecture

The project follows a clean **Separation of Concerns** architecture, ensuring the logic (`src`) is decoupled from assets (`templates`, `fonts`) and configuration.

```text
Mishkat/
│
├── config/             # YAML configurations (Non-code settings)
│   ├── fonts.yaml      # Font mappings and fallback rules
│   ├── paths.yaml      # Directory paths for I/O
│   └── video.yaml      # FFmpeg encoding settings (bitrate, fps)
│
├── fonts/              # Local font repository
│   ├── arabic/         # e.g., Amiri Quran
│   └── latin/          # e.g., DejaVu Serif
│
├── data/               # Data ingestion layer
│   ├── csv/            # Structured verses and metadata
│   └── audio/          # Audio assets (git-ignored)
│
├── templates/          # Source design files
│   └── QuranTemplate_BASE.pptx
│
├── src/                # Core Application Logic
│   ├── utils/          # Helper modules (I/O, String manipulation)
│   ├── slide/          # Slide rendering engine (PPTX manipulation)
│   ├── video/          # Video encoding wrapper (FFmpeg)
│   └── pipeline/       # High-level execution scripts
│
└── requirements.txt    # Python dependencies
```

---

## ⚙️ Prerequisites

Since Mishkat relies on system-level binaries for media processing, you must have the following installed:

1.  **Python 3.8+**
2.  **FFmpeg:** Required for video encoding and audio merging.
    *   *Linux:* `sudo apt install ffmpeg`
    *   *Mac:* `brew install ffmpeg`
    *   *Windows:* Add ffmpeg to your System PATH.
3.  **LibreOffice:** Required for headless conversion of slides to images.
    *   *Linux:* `sudo apt install libreoffice`

---

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/mishkat.git
    cd mishkat
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Fonts:**
    Ensure the fonts located in `fonts/` are installed on your operating system to prevent rendering artifacts.

---

## 🚀 Usage

Mishkat allows you to generate a video for a specific Ayah programmatically.

### Example: Generating a Single Verse Video

```python
import sys
import os

# Ensure src is in the python path
sys.path.append(os.getcwd())

from src.pipeline import create_ayah_video

# Run the pipeline
video_path = create_ayah_video(
    surah_name="Al-Kawthar",
    verse_number=1,
    ayah_text="إِنَّا أَعْطَيْنَاكَ الْكَوْثَرَ",
    translation_text="Indeed, We have granted you, [O Muhammad], al-Kawthar.",
    # ... other parameters
)

print(f"Video generated at: {video_path}")
```

---

## 🤝 Contributing

Contributions are welcome! We follow a standard GitHub flow:

1.  **Fork** the repository.
2.  Create a new **Branch** (`git checkout -b feature/NewTemplate`).
3.  **Commit** your changes.
4.  **Push** to the branch.
5.  Open a **Pull Request**.

Please ensure your code follows the existing structure and includes comments where necessary.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

<p align="center">
  <i>Developed with ❤️ for the service of the Holy Quran.</i>
</p>
