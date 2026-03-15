import re


def clean_text(text: str) -> str:
    """
    Basic cleaning for extracted PDF text.
    - Removes author markers
    - Collapses whitespace
    - Trims content before 'Abstract' when present
    """
    text = re.sub(r"∗|†|‡", "", text)

    if "Abstract" in text:
        text = text[text.index("Abstract"):]

    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_reference_heavy(text: str) -> bool:
    """
    Heuristic to detect reference-heavy chunks, even if section detection missed it.
    """
    lowered = text.lower()

    reference_signals = [
        "references",
        "arxiv preprint",
        "in proceedings of",
        "journal of",
        "conference on",
        "et al.",
    ]

    score = sum(signal in lowered for signal in reference_signals)
    return score >= 2


def is_noise_heavy(text: str) -> bool:
    """
    Heuristic to detect author-note / footer / contribution-noise chunks.
    """
    lowered = text.lower()

    noise_signals = [
        "equal contribution",
        "listing order is random",
        "work performed while at",
        "conference on neural information processing systems",
        "google brain",
        "google research",
        "university of toronto",
    ]

    score = sum(signal in lowered for signal in noise_signals)
    return score >= 2