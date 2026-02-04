from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
from datetime import datetime

# =========================================================
# INTERNAL MODULES
# =========================================================
from image_analysis.brushstroke import analyze_brushstrokes
from craquelure_analysis.crack_detector import analyze_craquelure
from decision_engine.decision_engine import compute_confidence
from report_engine.pdf_report import generate_pdf_report


# =========================================================
# PATH SETUP (single outputs folder at project root)
# =========================================================
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs"
REPORT_DIR = OUTPUT_DIR / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


# =========================================================
# FASTAPI INIT
# =========================================================
app = FastAPI(
    title="Art Authentication Decision Support System",
    description="Explainable, multi-signal AI-assisted artwork analysis",
    version="1.1.1"
)

# Serve generated artifacts
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")


# =========================================================
# ROOT
# =========================================================
@app.get("/")
def root():
    return {
        "message": "Art Authentication Decision Support System running",
        "status": "ok"
    }


# =========================================================
# BRUSHSTROKE ANALYSIS
# =========================================================
@app.post("/analyze/brushstrokes")
async def brushstroke_analysis(file: UploadFile = File(...)):
    temp_path = BASE_DIR / f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_brushstrokes(temp_path)

    return {
        "stroke_density": result["stroke_density"],
        "heatmap_url": f"http://127.0.0.1:8000/outputs/{result['heatmap_image'].name}",
        "note": result["note"]
    }


# =========================================================
# CRAQUELURE ANALYSIS
# =========================================================
@app.post("/analyze/craquelure")
async def craquelure_analysis(file: UploadFile = File(...)):
    temp_path = BASE_DIR / f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_craquelure(temp_path)

    return {
        "crack_density": result["crack_density"],
        "crack_overlay_url": f"http://127.0.0.1:8000/outputs/{result['crack_overlay'].name}",
        "note": result["note"]
    }


# =========================================================
# DECISION ENGINE (ADAPTIVE WEIGHTS + CONFIDENCE BANDS)
# =========================================================
@app.post("/analyze/decision")
async def decision_analysis(
    file: UploadFile = File(...),
    profile: str = "default"
):
    temp_path = BASE_DIR / f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    brush = analyze_brushstrokes(temp_path)
    crack = analyze_craquelure(temp_path)

    decision = compute_confidence(
        stroke_density=brush["stroke_density"],
        crack_density=crack["crack_density"],
        profile=profile
    )

    return {
        **decision,
        "visual_outputs": {
            "brushstroke_heatmap": f"http://127.0.0.1:8000/outputs/{brush['heatmap_image'].name}",
            "craquelure_overlay": f"http://127.0.0.1:8000/outputs/{crack['crack_overlay'].name}"
        }
    }


# =========================================================
# PDF REPORT GENERATION (PERMISSION-SAFE)
# =========================================================
@app.post("/analyze/report")
async def generate_report(
    file: UploadFile = File(...),
    profile: str = "default"
):
    temp_path = BASE_DIR / f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    brush = analyze_brushstrokes(temp_path)
    crack = analyze_craquelure(temp_path)

    decision = compute_confidence(
        stroke_density=brush["stroke_density"],
        crack_density=crack["crack_density"],
        profile=profile
    )

    # 🔥 FIX: UNIQUE PDF NAME (NO WINDOWS LOCK ISSUES)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = file.filename.replace(" ", "_")
    pdf_path = REPORT_DIR / f"report_{timestamp}_{safe_name}.pdf"

    generate_pdf_report(
        output_path=pdf_path,
        artwork_name=file.filename,
        decision_data=decision,
        heatmap_path=brush["heatmap_image"],
        crack_path=crack["crack_overlay"]
    )

    return {
        "message": "PDF report generated successfully",
        "confidence_index": decision["confidence_index"],
        "confidence_band": decision["confidence_band"],
        "profile_used": decision["profile_used"],
        "report_url": f"http://127.0.0.1:8000/outputs/reports/{pdf_path.name}"
    }
