from sqlalchemy import text
from app.services.embedding_service import EmbeddingService
from app.services.review_classifier_service import review_classifier_service

CATEGORIES = [
    "여성의류",
    "남성의류",
    "패션슈즈",
    "잡화",
]


def extract_category(question: str) -> str | None:
    for category in CATEGORIES:
        if category in question:
            return category

    return None

def detect_query_sentiment(question: str) -> str | None:
    q = question.lower()

    positive_words = [
        "만족", "장점", "좋은점", "좋은 점",
        "강점", "칭찬", "긍정", "좋았던",
    ]

    negative_words = [
        "불만", "문제", "이슈", "단점",
        "아쉬움", "아쉬운", "불편",
        "개선", "나쁜", "별로", "부정",
    ]

    if any(word in q for word in positive_words):
        return "positive"

    if any(word in q for word in negative_words):
        return "negative"

    return None

class ReviewRagService:

    @staticmethod
    def search(
        question: str,
        db,
        limit: int = 10,
        product_id: int | None = None,
        category: str | None = None
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

        if product_id is not None:
            where_conditions.append(
                "r.product_id = :product_id"
            )
            params["product_id"] = product_id
            
        if category is not None:
            where_conditions.append("p.category = :category")
            params["category"] = category
            
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
                        JOIN products p ON p.id = r.product_id
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
    
    @staticmethod
    def search_by_sentiment(
        question: str,
        db,
        sentiment: str,
        limit: int = 5,
        product_id: int | None = None,
        category: str | None = None
    ):
        query_embedding = EmbeddingService.embed(question)

        intent = review_classifier_service.predict(
            question,
            top_k=2,
        )
        query_tags = intent["tags"]

        where_conditions = [
            "r.sentiment = :sentiment"
        ]

        params = {
            "embedding": str(query_embedding),
            "sentiment": sentiment,
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

        if product_id is not None:
            where_conditions.append(
                "r.product_id = :product_id"
            )
            params["product_id"] = product_id
            
        if category is not None:
            where_conditions.append(
                "p.category = :category"
            )
            params["category"] = category

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
                    JOIN products p ON p.id = r.product_id
                    WHERE {where_clause}
                ) ranked
                WHERE rn = 1
                ORDER BY score
                LIMIT :limit
                """
            ),
            params,
        )

        return results.fetchall()