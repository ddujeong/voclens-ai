from collections import Counter

from app.core.voc_keywords import COMPLAINT_KEYWORDS
from app.models.review import Review


class AdminChatService:

    @staticmethod
    def analyze_top_complaint(reviews: list[Review]) -> str:

        counter = Counter()

        for review in reviews:
            for keyword in COMPLAINT_KEYWORDS:
                if keyword in review.content:
                    counter[keyword] += 1

        if not counter:
            return (
                "현재 분석 가능한 부정 리뷰가 부족합니다."
            )

        keyword, count = counter.most_common(1)[0]

        related_reviews = [
            review.content
            for review in reviews
            if keyword in review.content
        ]

        answer = (
            f"현재 가장 많이 언급되는 불만은 "
            f"'{keyword}'입니다.\n"
            f"총 {count}건 언급되었습니다.\n\n"
            f"관련 리뷰 예시:\n"
        )

        for review in related_reviews[:3]:
            answer += f"- {review}\n"

        return answer