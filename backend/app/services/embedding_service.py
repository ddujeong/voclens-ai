from sentence_transformers import SentenceTransformer


class EmbeddingService:

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    @classmethod
    def embed(
        cls,
        text: str,
    ) -> list[float]:

        return cls.model.encode(
            text
        ).tolist()