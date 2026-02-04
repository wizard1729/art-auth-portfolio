# 🎨 Art Authentication Decision Support System

An Explainable AI-powered decision support platform for artwork analysis, combining computer vision, adaptive intelligence, and forensic-style reporting.

This system is not an authenticity verdict engine. It assists curators, researchers, conservators, and galleries by providing interpretable visual and statistical signals.

## 🚀 Features

### 🔍 Visual Analysis
- Brushstroke Complexity Analysis
- Craquelure (Crack Pattern) Detection
- Visual heatmaps & overlays for transparency

### 🧠 Decision Engine
- Multi-signal fusion (brushstrokes + ageing patterns)
- Adaptive weights based on artist/era profiles

**Outputs:**
- Confidence Index (0–100)
- Confidence Band: Low / Medium / High
- Human-readable explanations

### 📄 PDF Forensic Report
- Auto-generated, shareable PDF per artwork
- Includes:
  - Confidence score & band
  - Explanations
  - Visual evidence (heatmap + cracks)
  - Disclaimer (decision support, not verdict)

### 🖥️ Frontend Dashboard
- Upload artwork
- Select artist/era profile
- View confidence instantly
- Download PDF report

## 🧩 Architecture Overview
- **Frontend (React)**
        |
        v
- **FastAPI Backend**
  - Image Analysis (OpenCV)
    - Brushstroke Module
    - Craquelure Module
  - Decision Engine
    - Adaptive Weights
    - Confidence Bands
  - Report Engine
    - PDF Generator (ReportLab)
  - Static Outputs (Images + PDFs)

## 📁 Project Structure
```
art-auth-portfolio/
├── backend/
│   ├── main.py
│   ├── image_analysis/
│   ├── craquelure_analysis/
│   ├── decision_engine/
│   └── report_engine/
├── frontend/
│   └── React Dashboard
├── outputs/
│   ├── heatmap_*.jpg
│   ├── cracks_*.jpg
│   └── reports/
│       └── report_*.pdf
└── README.md
```

## 🛠️ Tech Stack

### Backend
- Python 3.10+
- FastAPI
- OpenCV
- NumPy
- ReportLab

### Frontend
- React (Vite)
- CSS

## ⚙️ Setup Instructions

### 1️⃣ Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run backend:
uvicorn main:app --reload

# Swagger API:
http://127.0.0.1:8000/docs
```

### 2️⃣ Frontend Setup
```bash
cd frontend
npm install
npm run dev

# Frontend:
http://localhost:5173
```

## 🔗 API Endpoints
- **Analyze Brushstrokes**: `POST /analyze/brushstrokes`
- **Analyze Craquelure**: `POST /analyze/craquelure`
- **Decision Engine**: `POST /analyze/decision?profile=modern`
- **Generate PDF Report**: `POST /analyze/report?profile=renaissance`

## ⚠️ Disclaimer
This system provides decision support, not authentication verdicts. Outputs should be interpreted by trained professionals alongside historical, material, and provenance evidence.

## 🌱 Future Enhancements
- Provenance graph visualization
- Batch analysis for collections
- Artist-specific learned models
- Cloud deployment
- Role-based access (museum mode)

## 👨‍💻 Author
**Anurag Lal**  
Software Engineer