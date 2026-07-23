import re
from .preprocess import normalized_for_matching

# A deliberately editable, broad vocabulary. Multi-word phrases are matched first.
SKILL_CATALOG = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "r", "go", "rust",
    "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "streamlit",
    "html", "css", "tailwind", "bootstrap", "rest api", "graphql", "microservices",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "linux", "git", "github actions",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "machine learning", "deep learning",
    "nlp", "computer vision", "data analysis", "data visualization", "tableau", "power bi",
    "spark", "hadoop", "airflow", "dbt", "snowflake", "postgresql", "mysql", "mongodb", "redis",
    "agile", "scrum", "jira", "figma", "excel", "communication", "leadership", "project management",
]


def extract_skills(text: str) -> set[str]:
    haystack = normalized_for_matching(text)
    found = set()
    for skill in SKILL_CATALOG:
        escaped = re.escape(skill.lower())
        if re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", haystack):
            found.add(skill)
    return found
