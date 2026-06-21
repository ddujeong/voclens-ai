from sqlalchemy import text

from app.models.review_document import ReviewDocument
from app.services.embedding_service import EmbeddingService


class ReviewRagService:

    @staticmethod
    def search(
        question: str,
        db,
        limit: int = 5,
    ):
        query_embedding = EmbeddingService.embed(
            question
        )

        results = db.execute(
            text(
                """
                SELECT
                    id,
                    review_id,
                    content,
                    embedding <=> :embedding AS score
                FROM review_documents
                ORDER BY score
                LIMIT :limit
                """
            ),
            {
                "embedding": str(query_embedding),
                "limit": limit,
            },
        )

        return results.fetchall()