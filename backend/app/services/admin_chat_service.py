from app.services.gemini_service import GeminiService
from app.services.review_rag_service import (
    ReviewRagService,
    detect_query_sentiment,
)


class AdminChatService:

    @staticmethod
    def answer_with_rag(
        question: str,
        db,
        product_id: int | None = None,
        category: str | None = None
    ) -> str:

        sentiment_filter = detect_query_sentiment(question)
        gemini_service = GeminiService()

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
                    return "질문과 관련된 리뷰 데이터를 찾지 못했습니다."

                return gemini_service.generate_voc_comparison_report(
                    question=question,
                    positive_reviews=positive_reviews,
                    negative_reviews=negative_reviews,
                )

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
                return "질문과 관련된 리뷰 데이터를 찾지 못했습니다."

            review_text = "\n".join(
                f"- {review}"
                for review in related_reviews
            )

            return gemini_service.generate_voc_report(
                question=question,
                reviews=review_text,
            )

        except Exception as e:
            print(e)
            return "VOC 분석 중 오류가 발생했습니다."