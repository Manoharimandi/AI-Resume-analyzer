from .ats_score import Analysis


def make_suggestions(analysis: Analysis) -> list[str]:
    ideas = []
    if analysis.missing_skills:
        ideas.append("Add relevant evidence for: " + ", ".join(sorted(analysis.missing_skills)[:8]) + ".")
    if analysis.components["Sections"] < 100:
        ideas.append("Use clear, ATS-readable headings for Skills, Experience, and Education.")
    if analysis.components["Format & contact"] < 100:
        ideas.append("Include a professional email, phone number, and LinkedIn profile in the header.")
    if analysis.components["Experience"] < 80:
        ideas.append("Make relevant experience explicit, including years of experience and measurable outcomes.")
    if analysis.components["Semantic similarity"] < 60:
        ideas.append("Mirror the job description's terminology naturally in your summary and accomplishment bullets.")
    return ideas or ["Strong alignment. Tailor your top accomplishments to the role before applying."]
