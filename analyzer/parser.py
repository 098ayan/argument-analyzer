import re

def split_sentences(text: str) -> list[str]:
    """
    Split text into sentences while preserving logical flow.
    """
    text = text.strip()

    # Normalize newlines
    text = re.sub(r'\n+', ' ', text)

    # Split on sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [s.strip() for s in sentences if len(s.strip()) > 2]
