import re

# =====================================================
# Helper: Detect Arabic
# =====================================================
def is_arabic(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF]', text))

# =====================================================
# Helper: Dynamic Font Size Estimator
# =====================================================
def estimate_font_size(
    text: str,
    box_width_ratio: float,
    box_height_ratio: float,
    slide_width,
    slide_height,
    is_arabic_text: bool
) -> int:
    """
    Estimate appropriate font size based on text length and box size.
    """

    # Base limits
    max_size = 44 if is_arabic_text else 30
    min_size = 18 if is_arabic_text else 14

    # Logical text length (Arabic diacritics are ignored)
    logical_length = len(re.sub(r'[^\w\s]', '', text))

    # Effective box area
    box_area = (slide_width * box_width_ratio) * (slide_height * box_height_ratio)

    # Density heuristic
    density = logical_length / box_area

    # Scaling factor (empirically tuned)
    size = max_size - int(density * 1.2e7)

    return max(min_size, min(size, max_size))
