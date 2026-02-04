import cv2
import numpy as np
from pathlib import Path
import os

# ---------- PATH SETUP ----------
BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
# --------------------------------

def analyze_brushstrokes(image_path: Path):
    """
    Extracts brushstroke-like edge patterns and
    generates a visual heatmap overlay.

    This is NOT an authenticity verdict.
    """

    img_color = cv2.imread(str(image_path))
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(img_gray, 50, 150)

    stroke_density = np.sum(edges > 0) / edges.size

    heatmap = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img_color, 0.7, heatmap, 0.3, 0)

    output_path = OUTPUT_DIR / f"heatmap_{image_path.name}"
    cv2.imwrite(str(output_path), overlay)

    return {
        "stroke_density": round(float(stroke_density), 4),
        "heatmap_image": output_path,
        "note": "Heatmap highlights high-frequency brushstroke regions"
    }