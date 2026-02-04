from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from pathlib import Path
from datetime import datetime


def generate_pdf_report(
    output_path: Path,
    artwork_name: str,
    decision_data: dict,
    heatmap_path: Path,
    crack_path: Path
):
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    # ==========================
    # HEADER
    # ==========================
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, height - 2 * cm, "Art Authentication Decision Report")

    c.setFont("Helvetica", 10)
    c.drawString(
        2 * cm,
        height - 2.8 * cm,
        f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M')}"
    )

    # ==========================
    # ARTWORK INFO
    # ==========================
    y = height - 4.2 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Artwork Information")

    c.setFont("Helvetica", 11)
    c.drawString(2 * cm, y - 0.8 * cm, f"Artwork file: {artwork_name}")
    c.drawString(
        2 * cm,
        y - 1.6 * cm,
        f"Analysis profile: {decision_data['profile_used']}"
    )

    # ==========================
    # CONFIDENCE SCORE
    # ==========================
    y -= 3 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Decision Summary")

    c.setFont("Helvetica", 11)
    c.drawString(
        2 * cm,
        y - 0.9 * cm,
        f"Confidence Index: {decision_data['confidence_index']}%"
    )
    c.drawString(
        2 * cm,
        y - 1.7 * cm,
        f"Confidence Band: {decision_data['confidence_band']}"
    )

    # ==========================
    # EXPLANATION
    # ==========================
    y -= 3.2 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Explanation")

    c.setFont("Helvetica", 10.5)
    text = c.beginText(2 * cm, y - 1 * cm)
    for line in decision_data["explanation"]:
        text.textLine(f"- {line}")
    c.drawText(text)

    # ==========================
    # IMAGES
    # ==========================
    y -= 5.5 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Visual Analysis")

    c.drawImage(
        str(heatmap_path),
        2 * cm,
        y - 7 * cm,
        width=7 * cm,
        preserveAspectRatio=True,
        mask="auto"
    )

    c.drawImage(
        str(crack_path),
        11 * cm,
        y - 7 * cm,
        width=7 * cm,
        preserveAspectRatio=True,
        mask="auto"
    )

    # ==========================
    # DISCLAIMER
    # ==========================
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        2 * cm,
        1.8 * cm,
        decision_data["disclaimer"]
    )

    c.showPage()
    c.save()