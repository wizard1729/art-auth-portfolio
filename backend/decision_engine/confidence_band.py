# backend/decision_engine/confidence_band.py

def confidence_band(score: float) -> str:
    """
    Converts a numerical confidence score into
    a human-readable confidence band.
    """

    if score < 50:
        return "Low"
    elif score < 75:
        return "Medium"
    else:
        return "High"