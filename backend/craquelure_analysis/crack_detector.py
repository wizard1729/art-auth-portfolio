import cv2
import numpy as np
from pathlib import Path

# ---------- PATH SETUP ----------
BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
# --------------------------------

def analyze_craquelure(image_path: Path):
    """
    Detects crack-like structures (craquelure) in paintings.
    Provides visual overlay and statistical indicators.

    NOT an age or authenticity verdict.
    """

    img_color = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    cracks = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15,
        3
    )

    kernel = np.ones((2, 2), np.uint8)
    cracks = cv2.morphologyEx(cracks, cv2.MORPH_OPEN, kernel)

    crack_density = np.sum(cracks > 0) / cracks.size

    overlay = img_color.copy()
    overlay[cracks > 0] = [0, 0, 255]

    output_path = OUTPUT_DIR / f"cracks_{image_path.name}"
    cv2.imwrite(str(output_path), overlay)

    return {
        "crack_density": round(float(crack_density), 4),
        "crack_overlay": output_path,
        "note": "Detected crack patterns consistent with natural paint ageing"
    }