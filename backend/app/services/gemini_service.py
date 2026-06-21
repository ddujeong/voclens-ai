import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.1-flash-lite"

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY가 설정되지 않았습니다.")

        self.client = genai.Client(api_key=api_key)

    def generate_admin_answer(
        self,
        question: str,
        top_keyword: str,
        count: int,
        related_reviews: list[str],
    ) -> str:
        review_text = "\n".join(
            [f"- {review}" for review in related_reviews[:5]]
        )

        prompt = f"""
당신은 쇼핑몰 운영자를 돕는 VOC 분석 AI 에이전트입니다.

운영자의 질문:
{question}

분석 결과:
- 주요 불만 키워드: {top_keyword}
- 언급 횟수: {count}건

관련 리뷰:
{review_text}

답변 규칙:
1. 운영자가 바로 이해할 수 있게 요약합니다.
2. 고객 불만의 핵심 원인을 설명합니다.
3. 개선 우선순위를 제안합니다.
4. 과장하지 말고 제공된 리뷰 근거 안에서만 답변합니다.
"""

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text