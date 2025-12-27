from typing import List, Dict, Optional

def detect_ad_hominem(sentences: List[str]) -> List[Dict]:
    results = []
    insults = ("idiot", "stupid", "ignorant", "fool", "dumb")

    for s in sentences:
        lower = s.lower()
        if any(word in lower for word in insults):
            results.append({
                "type": "Ad Hominem",
                "sentence": s,
                "explanation": (
                    "Attacks a person or group instead of addressing "
                    "the actual argument."
                )
            })
    return results


def detect_strawman(sentences: List[str]) -> List[Dict]:
    results = []
    markers = (
        "they say that",
        "people claim that",
        "supporters believe that",
        "critics say that",
    )

    for s in sentences:
        lower = s.lower()
        if any(m in lower for m in markers):
            results.append({
                "type": "Strawman",
                "sentence": s,
                "explanation": (
                    "Misrepresents an opposing position to make it easier to attack."
                )
            })
    return results


def detect_false_dilemma(sentences: List[str]) -> List[Dict]:
    results = []
    markers = (
        "either",
        "only two options",
        "no other choice",
        "you must choose",
    )

    for s in sentences:
        lower = s.lower()
        if any(m in lower for m in markers):
            results.append({
                "type": "False Dilemma",
                "sentence": s,
                "explanation": (
                    "Presents limited options as if they were the only possibilities."
                )
            })
    return results


def detect_circular_reasoning(
    sentences: List[str],
    conclusion: Optional[str]
) -> List[Dict]:
    results = []
    if not conclusion:
        return results

    conclusion_lower = conclusion.lower()

    for s in sentences:
        if s == conclusion:
            continue
        if conclusion_lower in s.lower():
            results.append({
                "type": "Circular Reasoning",
                "sentence": s,
                "explanation": (
                    "The conclusion is assumed in the premises instead of being supported."
                )
            })
    return results


def detect_appeal_to_authority(sentences: List[str]) -> List[Dict]:
    results = []
    markers = (
        "experts say",
        "scientists say",
        "according to authority",
        "studies prove",
        "research shows",
    )

    for s in sentences:
        lower = s.lower()
        if any(m in lower for m in markers):
            results.append({
                "type": "Appeal to Authority",
                "sentence": s,
                "explanation": (
                    "Relies on authority as evidence without examining the reasoning."
                )
            })
    return results


def detect_all_fallacies(
    sentences: List[str],
    conclusion: Optional[str]
) -> List[Dict]:
    """
    Run all fallacy detectors and return combined results.
    """
    fallacies = []
    fallacies.extend(detect_ad_hominem(sentences))
    fallacies.extend(detect_strawman(sentences))
    fallacies.extend(detect_false_dilemma(sentences))
    fallacies.extend(detect_circular_reasoning(sentences, conclusion))
    fallacies.extend(detect_appeal_to_authority(sentences))
    return fallacies
