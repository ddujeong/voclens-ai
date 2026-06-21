from app.services.gemini_service import GeminiService
from app.services.review_rag_service import ReviewRagService


class AdminChatService:

    @staticmethod
    def answer_with_rag(
        question: str,
        db,
    ) -> str:
        rag_results = ReviewRagService.search(
            question=question,
            db=db,
            limit=5,
        )

        print("\n===== QUESTION =====")
        print(question)

        print("\n===== RAG RESULTS =====")

        for row in rag_results:
            print(row.content)
            print("score =", row.score)

        related_reviews = [
            row.content
            for row in rag_results
        ]

        if not related_reviews:
            return "질문과 관련된 리뷰 데이터를 찾지 못했습니다."

        try:
            gemini_service = GeminiService()

            return gemini_service.generate_rag_answer(
                question=question,
                related_reviews=related_reviews,
            )

        except Exception:
            answer = "관련 리뷰를 기반으로 요약한 결과입니다.\n\n"

            for review in related_reviews[:3]:
                answer += f"- {review}\n"

            return answer