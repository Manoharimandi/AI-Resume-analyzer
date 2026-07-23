from functools import lru_cache


@lru_cache(maxsize=1)
def _model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(resume_text: str, job_text: str) -> tuple[float, str]:
    """Return similarity on 0-100. Fall back to TF-IDF if model/download is unavailable."""
    try:
        model = _model()
        vectors = model.encode([resume_text, job_text], normalize_embeddings=True)
        score = float(vectors[0] @ vectors[1])
        return round(max(0, min(1, score)) * 100, 1), "SentenceTransformer (all-MiniLM-L6-v2)"
    except Exception:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        try:
            matrix = TfidfVectorizer(stop_words="english").fit_transform([resume_text, job_text])
            return round(float(cosine_similarity(matrix[0], matrix[1])[0, 0]) * 100, 1), "TF-IDF fallback"
        except ValueError:
            return 0.0, "No comparable text"
