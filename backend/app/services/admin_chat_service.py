from app.services.gemini_service import GeminiService
from app.services.review_rag_service import (
    ReviewRagService,
    detect_query_sentiment,
    extract_category
)
from app.services.admin_intent_service import AdminIntentService
from app.services.voc_insight_service import VocInsightService
from typing import Any

class AdminChatService:

    @staticmethod
    def answer_with_rag(
        question: str,
        db,
        product_id: int | None = None,
        category: str | None = None
    ) -> dict[str, Any]:

        intent = AdminIntentService.parse(question)

        intent_category = intent.get("category")
        intent_tag = intent.get("tag")
        action = intent.get("action")

        if category is None:
            category = intent_category or extract_category(question)
        
        gemini_service = GeminiService()

        if action == "risk_products":
            if category is None or intent_tag is None:
                return {
                    "answer": "카테고리와 VOC 항목을 확인하지 못했습니다. 예: 여성의류에서 사이즈 불만 많은 상품 찾아줘",
                    "risk_products": [],
                    "category": category,
                    "tag": intent_tag,
                }

            rows = VocInsightService.get_risk_products(
                category=category,
                tag=intent_tag,
                db=db,
            )

            if not rows:
                return {
                    "answer": f"{category} 카테고리에서 {intent_tag} 관련 부정 리뷰가 많은 상품을 찾지 못했습니다.",
                    "risk_products": [],
                    "category": category,
                    "tag": intent_tag,
                }

            return {
                "answer": f"{category} 카테고리에서 {intent_tag} 관련 부정 리뷰가 많은 상품입니다.",
                "risk_products": [
                    {
                        "product_id": row.product_id,
                        "product_name": row.product_name,
                        "category": row.category,
                        "negative_count": row.negative_count,
                    }
                    for row in rows
                ],
                "category": category,
                "tag": intent_tag,

            }
        sentiment_filter = detect_query_sentiment(question)

        try:
            if sentiment_filter is None:
                positive_results = ReviewRagService.search_by_sentiment(
                    question=question,
                    db=db,
                    sentiment="positive",
                    limit=5,
                    product_id=product_id,
                    category=category
                )

                negative_results = ReviewRagService.search_by_sentiment(
                    question=question,
                    db=db,
                    sentiment="negative",
                    limit=5,
                    product_id=product_id,
                    category=category
                )

                positive_reviews = [
                    row.content
                    for row in positive_results
                ]

                negative_reviews = [
                    row.content
                    for row in negative_results
                ]

                if not positive_reviews and not negative_reviews:
                    return {
                        "answer": "질문과 관련된 리뷰 데이터를 찾지 못했습니다.",
                        "risk_products": [],
                        "category": category,
                        "tag": intent_tag,
                    }

                return {
                    "answer": gemini_service.generate_voc_comparison_report(
                        question=question,
                        positive_reviews=positive_reviews,
                        negative_reviews=negative_reviews,
                    ),
                    "risk_products": [],
                    "category": category,
                    "tag": intent_tag,

                }

            rag_results = ReviewRagService.search(
                question=question,
                db=db,
                limit=5,
                product_id=product_id,
                category=category
            )

            related_reviews = [
                row.content
                for row in rag_results
            ]

            if not related_reviews:
                return {
                    "answer": "질문과 관련된 리뷰 데이터를 찾지 못했습니다.",
                    "risk_products": [],
                    "category": category,
                    "tag": intent_tag,
                }

            review_text = "\n".join(
                f"- {review}"
                for review in related_reviews
            )

            return {
                "answer": gemini_service.generate_voc_report(
                    question=question,
                    reviews=review_text,
                ),
                "risk_products": [],
                "category": category,
                "tag": intent_tag,
            }

        except Exception as e:
            print(e)
            return {
                "answer": "VOC 분석 중 오류가 발생했습니다.",
                "risk_products": [],
            }