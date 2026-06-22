from sqlalchemy import text
from app.services.embedding_service import EmbeddingService
from app.services.review_classifier_service import review_classifier_service

def detect_query_sentiment(question: str) -> str | None:
    negative_words = [
        "VOC", "voc", "불만", "문제", "이슈", "단점",
        "아쉬움", "아쉬운", "불편", "개선", "나쁜",
        "별로", "부정",
    ]

    positive_words = [
        "만족", "장점", "좋은점", "좋은 점",
        "강점", "칭찬", "긍정", "좋았던",
    ]

    if any(word in question for word in negative_words):
        return "negative"

    if any(word in question for word in positive_words):
        return "positive"

    return None

class ReviewRagService:

    @staticmethod
    def search(
        question: str,
        db,
        limit: int = 5,
    ):
        query_embedding = EmbeddingService.embed(question)

        intent = review_classifier_service.predict(question, top_k=2)
        query_tags = intent["tags"]
        sentiment_filter = detect_query_sentiment(question)

        print("QUESTION:", question)
        print("QUERY TAGS:", query_tags)
        print("SENTIMENT:", sentiment_filter)
        print("INTENT:", intent)

        where_conditions = []
        params = {
            "embedding": str(query_embedding),
            "limit": limit,
        }

        if query_tags:
            tag_conditions = []

            for idx, tag in enumerate(query_tags):
                tag_conditions.append(
                    f"r.tags ILIKE :tag_{idx}"
                )
                params[f"tag_{idx}"] = f"%{tag}%"

            where_conditions.append(
                "(" + " OR ".join(tag_conditions) + ")"
            )

        if sentiment_filter:
            where_conditions.append(
                "r.sentiment = :sentiment"
            )
            params["sentiment"] = sentiment_filter

        if where_conditions:
            where_clause = " AND ".join(where_conditions)

            results = db.execute(
                text(
                    f"""
                    SELECT
                        id,
                        review_id,
                        content,
                        score
                    FROM (
                        SELECT
                            rd.id,
                            rd.review_id,
                            rd.content,
                            rd.embedding <=> :embedding AS score,
                            ROW_NUMBER() OVER (
                                PARTITION BY rd.content
                                ORDER BY rd.embedding <=> :embedding
                            ) AS rn
                        FROM review_documents rd
                        JOIN reviews r ON r.id = rd.review_id
                        WHERE {where_clause}
                    ) ranked
                    WHERE rn = 1
                    ORDER BY score
                    LIMIT :limit
                    """
                ),
                params,
            )

            rows = results.fetchall()

            if rows:
                return rows

        results = db.execute(
            text(
                """
                SELECT
                    id,
                    review_id,
                    content,
                    score
                FROM (
                    SELECT
                        id,
                        review_id,
                        content,
                        embedding <=> :embedding AS score,
                        ROW_NUMBER() OVER (
                            PARTITION BY content
                            ORDER BY embedding <=> :embedding
                        ) AS rn
                    FROM review_documents
                ) ranked
                WHERE rn = 1
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