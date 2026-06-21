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
    
    def generate_rag_answer(
        self,
        question: str,
        related_reviews: list[str],
    ) -> str:

        review_text = "\n".join(
            [f"- {review}" for review in related_reviews]
        )

        prompt = f"""
    당신은 쇼핑몰 운영자를 위한 VOC 분석 AI 에이전트입니다.

    운영자 질문:
    {question}

    검색된 관련 리뷰:
    {review_text}

    답변 규칙:
    1. 리뷰를 근거로만 답변합니다.
    2. 핵심 불만 또는 만족 포인트를 요약합니다.
    3. 개선 우선순위를 제안합니다.
    4. 리뷰에 없는 내용은 추측하지 않습니다.
    """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        return response.text
    
    def analyze_review_sentiment(
        self,
        content: str,
    ) -> str:
        prompt = f"""
    다음 쇼핑몰 리뷰의 감성을 분류하세요.

    리뷰:
    {content}

    분류 기준:
    - positive: 만족, 장점, 긍정 평가
    - negative: 불만, 문제점, 개선 필요
    - neutral: 긍정과 부정이 섞이거나 판단이 애매함

    반드시 아래 셋 중 하나만 출력하세요.
    positive
    negative
    neutral
    """

        response = self.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        sentiment = response.text.strip().lower()

        if sentiment not in ["positive", "negative", "neutral"]:
            return "neutral"

        return sentiment