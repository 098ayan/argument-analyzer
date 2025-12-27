from typing import List, Dict, Optional

# -------------------------------------------------
# Counter-argument detection (DISCOURSE + STRUCTURE)
# -------------------------------------------------
def detect_counter_arguments(
    sentences: List[str],
    conclusion: Optional[str] = None,
    premises: Optional[List[str]] = None
) -> List[Dict]:
    """
    Detect counter-arguments and classify them as:
    - rebuttal (attacks conclusion)
    - undercutter (attacks premise)
    """

    objections = []

    discourse_rebuttals = [
        "however", "but", "although", "yet"
    ]

    for s in sentences:
        s_clean = s.strip()
        s_lower = s_clean.lower()

        # --- Rebuttal via discourse marker ---
        if any(s_lower.startswith(m) for m in discourse_rebuttals):
            objections.append({
                "sentence": s_clean,
                "type": "rebuttal",
                "target": "conclusion",
                "explanation": "Discourse marker indicates rebuttal."
            })
            continue

        # --- Undercutter: challenges a premise ---
        if premises:
            for p in premises:
                if p.lower() in s_lower:
                    objections.append({
                        "sentence": s_clean,
                        "type": "undercutter",
                        "target": "premise",
                        "explanation": "Challenges the validity or relevance of a premise."
                    })
                    break

    return objections
