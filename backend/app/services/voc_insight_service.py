from sqlalchemy import text
import math


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
                    p.id AS product_id,
                    p.name AS product_name,
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

        rows = result.fetchall()

        risk_products = []

        for row in rows:
            risk_score = round(
                row.negative_count * math.log(row.negative_count + 1),
                1,
            )

            risk_products.append({
                "product_id": row.product_id,
                "product_name": row.product_name,
                "category": row.category,
                "negative_count": row.negative_count,
                "risk_score": risk_score,
            })

        return risk_products