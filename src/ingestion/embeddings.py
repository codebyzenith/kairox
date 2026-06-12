from sentence_transformers import SentenceTransformer

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def generate_embedding(headline: str, summary: str) -> list[float]:
    text = f"{headline}. {summary}"
    model = get_model()
    vector = model.encode(text)
    return vector.tolist()