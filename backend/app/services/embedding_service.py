from sentence_transformers import SentenceTransformer


class EmbeddingService:
    model = None

    @classmethod
    def get_model(cls):
        if cls.model is None:
            cls.model = SentenceTransformer(
                "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
            )

        return cls.model

    @classmethod
    def embed(
        cls,
        text: str,
    ) -> list[float]:
        model = cls.get_model()
        return model.encode(text).tolist()