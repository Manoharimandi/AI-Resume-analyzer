# AI Resume Analyzer & ATS Score Checker

> A beginner-friendly NLP project that helps students tailor their resumes to a job description.

This is my Python and Streamlit project for exploring how resume screening tools can compare a resume with a job description. Upload a PDF or DOCX resume, paste a job description, and the app shows an ATS-style score, matching skills, missing skills, suggestions, and a downloadable report.

**Note:** This project is for learning and resume improvement only. It does not make hiring decisions.

## What I built

- PDF and DOCX resume upload
- Text extraction and basic preprocessing
- Skill matching for technologies, tools, and workplace skills
- Semantic similarity using `all-MiniLM-L6-v2`
- Transparent ATS-style scoring
- Missing-skill suggestions
- Interactive score chart
- Downloadable PDF report

## How it works

1. The app reads the resume text from the uploaded file.
2. It extracts recognised skills from the resume and job description.
3. It compares both texts using semantic similarity.
4. It combines the results into an ATS-style score.
5. It highlights skills that can be added or explained better.

## Tech stack

| Area | Tools used |
| --- | --- |
| Language | Python |
| Interface | Streamlit |
| Resume parsing | pdfplumber, python-docx |
| Data & charts | pandas, Plotly |
| NLP | sentence-transformers, scikit-learn |
| Report export | ReportLab |

## ATS-style score

| Component | Weight |
| --- | ---: |
| Semantic similarity | 40% |
| Skill match | 25% |
| Education | 10% |
| Experience | 10% |
| Resume sections | 10% |
| Formatting and contact details | 5% |

The score is intentionally transparent so that it is easy to understand and improve.

## Project structure

```text
AI-Resume-Analyzer/
├── app.py                 # Streamlit user interface
├── requirements.txt       # Project dependencies
└── utils/
    ├── parser.py          # PDF/DOCX text extraction
    ├── preprocess.py      # Text cleanup
    ├── skills.py          # Skill vocabulary and matching
    ├── embeddings.py      # Semantic similarity
    ├── ats_score.py       # ATS-style score calculation
    ├── suggestions.py     # Resume improvement tips
    └── report.py          # PDF report generation
```

## Run the project locally

```bash
git clone https://github.com/Manoharimandi/AI-Resume-analyzer.git
cd AI-Resume-analyzer

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install -r requirements.txt
python3 -m pip install torch torchvision

streamlit run app.py --server.fileWatcherType none
```

Open the local URL shown in Terminal, usually `http://localhost:8501`.

## What I learned

- Building a web app with Streamlit
- Reading text from PDF and DOCX files
- Basic NLP preprocessing and skill extraction
- Cosine similarity and sentence embeddings
- Designing a weighted scoring system
- Creating downloadable reports with Python
- Using Git and GitHub to publish a project

## Future improvements

- Add a larger skills database for different job roles
- Support more resume file formats
- Let users customise the scoring weights
- Add job-role-specific feedback
- Deploy the project using Streamlit Community Cloud

## Author

**Manohar Imandi**


