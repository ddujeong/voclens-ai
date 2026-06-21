from sentence_transformers import SentenceTransformer


class EmbeddingService:

    model = SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    @classmethod
    def embed(
        cls,
        text: str,
    ) -> list[float]:
        return cls.model.encode(text).tolist()