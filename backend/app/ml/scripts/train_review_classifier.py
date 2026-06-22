import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer


DATA_PATH = (
    Path(__file__).parents[1]
    / "data"
    / "fashion_training_dataset.json"
)

MODEL_DIR = (
    Path(__file__).parents[1]
    / "models"
)

TAG_MODEL_PATH = MODEL_DIR / "tag_classifier.joblib"
SENTIMENT_MODEL_PATH = MODEL_DIR / "sentiment_classifier.joblib"
TAG_BINARIZER_PATH = MODEL_DIR / "tag_binarizer.joblib"


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    texts = [
        item["text"]
        for item in data
        if item.get("text")
    ]

    tags = [
        item["tags"]
        for item in data
        if item.get("text")
    ]

    sentiments = [
        item["sentiment"]
        for item in data
        if item.get("text")
    ]

    tag_binarizer = MultiLabelBinarizer()
    tag_labels = tag_binarizer.fit_transform(tags)

    X_train, X_test, y_tags_train, y_tags_test, y_sent_train, y_sent_test = train_test_split(
        texts,
        tag_labels,
        sentiments,
        test_size=0.2,
        random_state=42,
        stratify=sentiments,
    )

    tag_model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95,
            ),
        ),
        (
            "clf",
            MultiOutputClassifier(
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                )
            ),
        ),
    ])

    sentiment_model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95,
            ),
        ),
        (
            "clf",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
            ),
        ),
    ])

    print("태그 분류 모델 학습 중...")
    tag_model.fit(X_train, y_tags_train)

    print("감성 분류 모델 학습 중...")
    sentiment_model.fit(X_train, y_sent_train)

    print("\n감성 분류 평가")
    y_sent_pred = sentiment_model.predict(X_test)
    print(classification_report(y_sent_test, y_sent_pred))

    print("\n태그 분류 전체 평가")

    y_tag_pred = tag_model.predict(X_test)

    print(
        classification_report(
            y_tags_test,
            y_tag_pred,
            target_names=tag_binarizer.classes_,
            zero_division=0,
        )
    )

    print(
        "micro f1:",
        f1_score(y_tags_test, y_tag_pred, average="micro")
    )

    print(
        "macro f1:",
        f1_score(y_tags_test, y_tag_pred, average="macro")
    )
    print("\n태그 분류 샘플 평가")
    y_tag_pred = tag_model.predict(X_test[:10])

    for text, true_tags, pred_tags in zip(
        X_test[:10],
        y_tags_test[:10],
        y_tag_pred,
    ):
        true_tag_names = tag_binarizer.inverse_transform(
            true_tags.reshape(1, -1)
        )[0]

        pred_tag_names = tag_binarizer.inverse_transform(
            pred_tags.reshape(1, -1)
        )[0]

        print("-" * 80)
        print("리뷰:", text)
        print("정답:", list(true_tag_names))
        print("예측:", list(pred_tag_names))

    joblib.dump(tag_model, TAG_MODEL_PATH)
    joblib.dump(sentiment_model, SENTIMENT_MODEL_PATH)
    joblib.dump(tag_binarizer, TAG_BINARIZER_PATH)

    print("\n모델 저장 완료")
    print(TAG_MODEL_PATH)
    print(SENTIMENT_MODEL_PATH)
    print(TAG_BINARIZER_PATH)


if __name__ == "__main__":
    main()