from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ----------------------------
# Tiny seed dataset
# ----------------------------
TRAIN_TEXTS = [
    "therefore the universe has a cause",
    "thus we should accept this view",
    "because it contradicts religion",
    "since it has strong evidence",
    "however this is false",
    "but this argument fails",
]

TRAIN_LABELS = [
    "conclusion",
    "conclusion",
    "premise",
    "premise",
    "rebuttal",
    "rebuttal",
]

# ----------------------------
# Train model once
# ----------------------------
_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
_X = _vectorizer.fit_transform(TRAIN_TEXTS)

_model = LogisticRegression(max_iter=1000)
_model.fit(_X, TRAIN_LABELS)

# ----------------------------
# Public API
# ----------------------------
def ml_classify_clause(text: str) -> Tuple[str, float]:
    """
    Returns (label, confidence)
    """
    vec = _vectorizer.transform([text])
    probs = _model.predict_proba(vec)[0]
    label = _model.classes_[probs.argmax()]
    confidence = probs.max()
    return label, confidence
