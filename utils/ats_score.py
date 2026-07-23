import re
from dataclasses import dataclass


@dataclass
class Analysis:
    score: float
    components: dict[str, float]
    resume_skills: set[str]
    job_skills: set[str]
    matched_skills: set[str]
    missing_skills: set[str]
    model_used: str


SECTION_PATTERNS = {
    "Experience": r"\b(experience|employment|work history)\b",
    "Education": r"\beducation\b",
    "Skills": r"\b(skills|technical skills|competencies)\b",
}


def _section_score(text: str) -> float:
    hits = sum(bool(re.search(pattern, text, re.I)) for pattern in SECTION_PATTERNS.values())
    return hits / len(SECTION_PATTERNS) * 100


def _education_score(resume: str, job: str) -> float:
    requested = bool(re.search(r"\b(bachelor|master|degree|b\.s\.|m\.s\.|phd)\b", job, re.I))
    present = bool(re.search(r"\b(bachelor|master|degree|b\.s\.|m\.s\.|phd)\b", resume, re.I))
    return 100.0 if present and (requested or present) else 0.0


def _experience_score(resume: str, job: str) -> float:
    def years(text):
        values = [int(x) for x in re.findall(r"(\d{1,2})\+?\s*(?:years|yrs)", text, re.I)]
        return max(values, default=0)
    wanted, have = years(job), years(resume)
    if not wanted:
        return 100.0 if have else 60.0
    return min(100.0, have / wanted * 100)


def _format_contact_score(resume: str) -> float:
    checks = [r"[\w.+-]+@[\w-]+\.[\w.-]+", r"(?:\+?\d[\d .()-]{7,}\d)", r"linkedin\.com"]
    return sum(bool(re.search(p, resume, re.I)) for p in checks) / len(checks) * 100


def build_analysis(resume: str, job: str, resume_skills: set[str], job_skills: set[str], semantic: float, model: str) -> Analysis:
    matched = resume_skills & job_skills
    skill_score = (len(matched) / len(job_skills) * 100) if job_skills else 50.0
    components = {
        "Semantic similarity": semantic,
        "Skill match": skill_score,
        "Education": _education_score(resume, job),
        "Experience": _experience_score(resume, job),
        "Sections": _section_score(resume),
        "Format & contact": _format_contact_score(resume),
    }
    weights = {"Semantic similarity": .40, "Skill match": .25, "Education": .10, "Experience": .10, "Sections": .10, "Format & contact": .05}
    total = sum(components[key] * weights[key] for key in weights)
    return Analysis(round(total, 1), {k: round(v, 1) for k, v in components.items()}, resume_skills, job_skills, matched, job_skills - resume_skills, model)
