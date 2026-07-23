from io import BytesIO
from pathlib import Path

import pdfplumber
from docx import Document


def extract_resume_text(uploaded_file) -> str:
    """Extract text from a Streamlit UploadedFile (PDF or DOCX)."""
    suffix = Path(uploaded_file.name).suffix.lower()
    payload = uploaded_file.getvalue()
    if suffix == ".pdf":
        with pdfplumber.open(BytesIO(payload)) as pdf:
            return "\n".join((page.extract_text() or "") for page in pdf.pages).strip()
    if suffix == ".docx":
        document = Document(BytesIO(payload))
        return "\n".join(p.text for p in document.paragraphs).strip()
    raise ValueError("Please upload a PDF or DOCX resume.")
