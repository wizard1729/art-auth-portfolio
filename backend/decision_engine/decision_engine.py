# backend/decision_engine/decision_engine.py

from typing import Dict
from decision_engine.confidence_band import confidence_band
from decision_engine.weight_profiles import WEIGHT_PROFILES


def compute_confidence(
    stroke_density: float,
    crack_density: float,
    profile: str = "default"
) -> Dict:
    """
    Combines multiple visual indicators into a single
    explainable confidence index using adaptive weights.

    profile: default | modern | renaissance | contemporary
    """

    # -------------------------------
    # Select weight profile
    # -------------------------------
    weights = WEIGHT_PROFILES.get(profile, WEIGHT_PROFILES["default"])
    WEIGHT_STROKE = weights["brushstroke"]
    WEIGHT_CRACK = weights["crack"]

    # -------------------------------
    # Normalization (empirical ranges)
    # -------------------------------

    stroke_score = min(stroke_density / 0.20, 1.0)

    if crack_density < 0.05:
        crack_score = 0.3
        crack_reason = "Very low crack density (possibly too uniform)"
    elif crack_density <= 0.35:
        crack_score = 1.0
        crack_reason = "Crack density consistent with natural ageing"
    else:
        crack_score = 0.5
        crack_reason = "Excessive crack density (possible stress or restoration)"

    # -------------------------------
    # Weighted fusion (ADAPTIVE)
    # -------------------------------
    confidence = (
        WEIGHT_STROKE * stroke_score +
        WEIGHT_CRACK * crack_score
    ) * 100

    confidence = round(confidence, 2)

    # -------------------------------
    # Confidence Band
    # -------------------------------
    band = confidence_band(confidence)

    # -------------------------------
    # Explanation
    # -------------------------------
    explanation = []

    explanation.append(
        f"Decision weights adapted for profile: '{profile}'."
    )

    if stroke_score > 0.7:
        explanation.append(
            "Brushstroke complexity aligns with known artistic techniques."
        )
    else:
        explanation.append(
            "Brushstroke signal is relatively weak or uniform."
        )

    explanation.append(crack_reason)

    return {
        "confidence_index": confidence,
        "confidence_band": band,
        "profile_used": profile,
        "signal_breakdown": {
            "brushstroke_score": round(stroke_score, 2),
            "crack_score": round(crack_score, 2)
        },
        "weights": {
            "brushstroke_weight": WEIGHT_STROKE,
            "crack_weight": WEIGHT_CRACK
        },
        "explanation": explanation,
        "disclaimer": "This score provides decision support, not an authenticity verdict."
    }