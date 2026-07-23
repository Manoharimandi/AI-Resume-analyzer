import re


def clean_text(text: str) -> str:
    """Normalize text while retaining meaningful technical tokens such as C++ and .NET."""
    text = text or ""
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[\t\r\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def normalized_for_matching(text: str) -> str:
    text = clean_text(text).lower()
    return re.sub(r"[^a-z0-9+#.\-/ ]", " ", text)
