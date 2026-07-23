import pandas as pd
import plotly.express as px
import streamlit as st

from utils.parser import extract_resume_text
from utils.preprocess import clean_text
from utils.skills import extract_skills
from utils.embeddings import semantic_similarity
from utils.ats_score import build_analysis
from utils.suggestions import make_suggestions
from utils.report import build_pdf_report

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("AI Resume Analyzer & ATS Score Checker")
st.caption("Compare a PDF or DOCX resume against a job description with transparent, editable scoring.")

with st.sidebar:
    st.header("How scoring works")
    st.write("Semantic 40%, Skills 25%, Education 10%, Experience 10%, Sections 10%, Format/contact 5%.")
    st.info("Scores are advisory, not a hiring decision. Never use this tool to make employment decisions.")

left, right = st.columns(2)
with left:
    uploaded = st.file_uploader("Upload resume", type=["pdf", "docx"])
with right:
    job_description = st.text_area("Paste job description", height=220, placeholder="Paste the role, responsibilities, and requirements here...")

if st.button("Analyze resume", type="primary", disabled=not (uploaded and job_description.strip())):
    try:
        with st.spinner("Extracting and comparing content..."):
            resume_text = clean_text(extract_resume_text(uploaded))
            job_text = clean_text(job_description)
            if not resume_text:
                raise ValueError("No readable text was found in this file. Try a text-based PDF or DOCX.")
            resume_skills, job_skills = extract_skills(resume_text), extract_skills(job_text)
            semantic, model = semantic_similarity(resume_text, job_text)
            analysis = build_analysis(resume_text, job_text, resume_skills, job_skills, semantic, model)
            suggestions = make_suggestions(analysis)
        st.session_state.update(analysis=analysis, suggestions=suggestions)
    except Exception as exc:
        st.error(str(exc))

if "analysis" in st.session_state:
    analysis, suggestions = st.session_state.analysis, st.session_state.suggestions
    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("ATS score", f"{analysis.score}/100")
    c2.metric("Matched skills", len(analysis.matched_skills), f"of {len(analysis.job_skills)} requested")
    c3.metric("Semantic similarity", f"{analysis.components['Semantic similarity']}%")
    st.caption(f"Similarity: {analysis.model_used}")
    chart_data = pd.DataFrame({"Category": list(analysis.components), "Score": list(analysis.components.values())})
    st.plotly_chart(px.bar(chart_data, x="Category", y="Score", range_y=[0, 100], color="Score", color_continuous_scale="Teal", title="Score breakdown"), use_container_width=True)
    a, b = st.columns(2)
    a.subheader("Matched skills")
    a.write(", ".join(sorted(analysis.matched_skills)) or "No direct skill matches detected.")
    b.subheader("Missing job skills")
    b.write(", ".join(sorted(analysis.missing_skills)) or "No catalogued skills missing.")
    st.subheader("Suggestions")
    for item in suggestions:
        st.write("• " + item)
    st.download_button("Download PDF report", data=build_pdf_report(analysis, suggestions), file_name="resume-analysis-report.pdf", mime="application/pdf")
