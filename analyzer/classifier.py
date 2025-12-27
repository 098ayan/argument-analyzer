from typing import List, Tuple, Optional

# -------------------------------------------------
# Optional ML import (SAFE)
# -------------------------------------------------
try:
    from analyzer.ml_classifier import ml_classify_clause
    ML_AVAILABLE = True
except Exception:
    ML_AVAILABLE = False


# -------------------------------------------------
# Utility: split compound sentences
# -------------------------------------------------
def split_compound(sentence: str) -> Tuple[str, Optional[str]]:
    """
    Split sentences of the form:
    'X because Y'
    Returns (X, Y) or (sentence, None)
    """
    lowered = sentence.lower()

    if " because " in lowered:
        idx = lowered.index(" because ")
        head = sentence[:idx].strip()
        tail = sentence[idx + len(" because "):].strip()
        return head, tail

    return sentence.strip(), None


# -------------------------------------------------
# Conclusion detection (RULES FIRST, ML OPTIONAL)
# -------------------------------------------------
def detect_conclusion_with_confidence(
    sentences: List[str],
    use_ml: bool = False
):
    """
    Detect the most likely conclusion.
    ML assists ONLY if use_ml=True.
    """

    explicit_markers = [
        "therefore", "thus", "hence", "it follows that", "so "
    ]

    objection_starters = [
        "however", "but", "although", "yet"
    ]

    # 1️⃣ Explicit conclusion markers
    for s in sentences:
        s_lower = s.lower()
        if any(m in s_lower for m in explicit_markers):
            return s.strip(), 0.9, []

    # 2️⃣ First assertive non-objection sentence
    for s in sentences:
        s_lower = s.lower().strip()

        if any(s_lower.startswith(m) for m in objection_starters):
            continue

        if s.strip().endswith("?"):
            continue

        head, _ = split_compound(s)
        return head.strip(), 0.6, []

    # 3️⃣ ML-assisted fallback (ONLY if enabled)
    if use_ml and ML_AVAILABLE:
        for s in sentences:
            label, conf = ml_classify_clause(s)
            if label == "conclusion" and conf > 0.6:
                return s.strip(), conf, []

    # 4️⃣ No conclusion found
    return None, 0.0, []


# -------------------------------------------------
# Premise extraction (CLAUSE-AWARE)
# -------------------------------------------------
def extract_premises(
    sentences: List[str],
    conclusion: Optional[str]
):
    """
    Extract premises from:
    - 'because' clauses
    - supporting sentences distinct from conclusion
    """
    premises = []

    for s in sentences:
        head, tail = split_compound(s)

        # Clause-based premise
        if tail:
            premises.append(tail.strip())
            continue

        # Sentence-based premise
        if conclusion and head.strip() != conclusion.strip():
            premises.append(head.strip())

    return premises
