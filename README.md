# AI Resume Analyzer & ATS Score Checker

A Streamlit app that analyzes a PDF/DOCX resume against a pasted job description. It extracts known skills, measures semantic similarity with `all-MiniLM-L6-v2` when available, uses a transparent weighted ATS-style score, and exports a PDF report.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

The first semantic analysis may download the transformer model. If that is unavailable, the app automatically uses a local TF-IDF similarity fallback.

## Score components

| Component | Weight |
| --- | ---: |
| Semantic similarity | 40% |
| Skill match | 25% |
| Education | 10% |
| Experience | 10% |
| Resume sections | 10% |
| Formatting & contact | 5% |

The score is a tailoring aid only and must not be used as an automated employment decision.
