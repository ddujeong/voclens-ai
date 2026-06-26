from app.services.gemini_service import GeminiService


class AdminIntentService:

    @staticmethod
    def parse(
        question: str,
    ) -> dict:
        gemini_service = GeminiService()

        return gemini_service.parse_admin_intent(
            question=question,
        )