from sqlalchemy import text


class VocInsightService:

    @staticmethod
    def get_risk_products(
        category: str,
        tag: str,
        db,
        limit: int = 10,
    ):
        result = db.execute(
            text(
                """
                SELECT
                    p.id,
                    p.name,
                    p.category,
                    COUNT(*) AS negative_count
                FROM reviews r
                JOIN products p
                    ON p.id = r.product_id
                WHERE p.category = :category
                  AND r.sentiment = 'negative'
                  AND r.tags ILIKE :tag
                GROUP BY
                    p.id,
                    p.name,
                    p.category
                ORDER BY negative_count DESC
                LIMIT :limit
                """
            ),
            {
                "category": category,
                "tag": f"%{tag}%",
                "limit": limit,
            },
        )

        return result.fetchall()