from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from .ats_score import Analysis


def build_pdf_report(analysis: Analysis, suggestions: list[str]) -> bytes:
    out = BytesIO()
    doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=42, rightMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    story = [Paragraph("AI Resume Analyzer Report", styles["Title"]), Spacer(1, 12)]
    story.append(Paragraph(f"Overall ATS score: <b>{analysis.score}/100</b>", styles["Heading2"]))
    story.append(Paragraph(f"Similarity method: {analysis.model_used}", styles["BodyText"]))
    rows = [["Category", "Score"]] + [[name, f"{score}/100"] for name, score in analysis.components.items()]
    table = Table(rows, colWidths=[300, 130])
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), .4, colors.lightgrey), ("PADDING", (0, 0), (-1, -1), 7)]))
    story += [Spacer(1, 12), table, Spacer(1, 14), Paragraph("Matched skills", styles["Heading2"]), Paragraph(", ".join(sorted(analysis.matched_skills)) or "None identified", styles["BodyText"]), Spacer(1, 10), Paragraph("Suggestions", styles["Heading2"])]
    story += [Paragraph("- " + item, styles["BodyText"]) for item in suggestions]
    doc.build(story)
    return out.getvalue()
