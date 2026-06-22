from pathlib import Path

import joblib


MODEL_DIR = (
    Path(__file__).parents[1]
    / "ml"
    / "models"
)


class ReviewClassifierService:
    def __init__(self):
        self.tag_model = joblib.load(
            MODEL_DIR / "tag_classifier.joblib"
        )
        self.sentiment_model = joblib.load(
            MODEL_DIR / "sentiment_classifier.joblib"
        )
        self.tag_binarizer = joblib.load(
            MODEL_DIR / "tag_binarizer.joblib"
        )

    def predict(
        self,
        text: str,
        threshold: float = 0.35,
        top_k: int = 2,
    ) -> dict:
        tag_probabilities = self.tag_model.predict_proba([text])

        tag_scores = []

        for idx, probabilities in enumerate(tag_probabilities):
            positive_probability = probabilities[0][1]

            tag_scores.append(
                (
                    self.tag_binarizer.classes_[idx],
                    float(positive_probability),
                )
            )

        tag_scores.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        top_score = tag_scores[0][1]

        tags = [
            tag
            for tag, score in tag_scores[:top_k]
            if score >= threshold and score >= top_score * 0.6
        ]

        sentiment = str(
            self.sentiment_model.predict([text])[0]
        )

        return {
            "tags": tags,
            "sentiment": sentiment,
            "tag_scores": tag_scores[:top_k],
        }


review_classifier_service = ReviewClassifierService()