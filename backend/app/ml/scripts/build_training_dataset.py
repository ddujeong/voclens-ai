import json
from pathlib import Path


INPUT_PATH = (
    Path(__file__).parents[1]
    / "data"
    / "fashion_labeled_reviews.json"
)

OUTPUT_PATH = (
    Path(__file__).parents[1]
    / "data"
    / "fashion_training_dataset.json"
)

ASPECT_NORMALIZE_MAP = {
    "치수/사이즈": "사이즈",
    "사이즈/폭/길이/두께": "사이즈",
    "기능성": "기능",
    "사용성/편의성": "사용성",
}

POLARITY_MAP = {
    "1": "positive",
    "-1": "negative",
    "0": "neutral",
}


def normalize_aspect(aspect: str) -> str:
    return ASPECT_NORMALIZE_MAP.get(
        aspect,
        aspect,
    )


def convert_polarity(value: str) -> str:
    return POLARITY_MAP.get(
        str(value),
        "neutral",
    )


def main():
    with open(INPUT_PATH, encoding="utf-8") as f:
        raw_data = json.load(f)

    dataset = []

    for item in raw_data:
        text = item.get("RawText", "").strip()

        if not text:
            continue

        tags = []

        aspect_sentiments = []

        for aspect_item in item.get("Aspects", []):
            aspect = normalize_aspect(
                aspect_item.get("Aspect", "").strip()
            )

            polarity = convert_polarity(
                aspect_item.get("SentimentPolarity")
            )

            if not aspect:
                continue

            tags.append(aspect)

            aspect_sentiments.append(
                {
                    "aspect": aspect,
                    "sentiment": polarity,
                    "text": aspect_item.get(
                        "SentimentText",
                        "",
                    ).strip(),
                }
            )

        tags = sorted(list(set(tags)))

        sentiment = convert_polarity(
            item.get("GeneralPolarity")
        )

        dataset.append(
            {
                "text": text,
                "tags": tags,
                "sentiment": sentiment,
                "aspect_sentiments": aspect_sentiments,
                "domain": item.get("Domain"),
                "category": item.get("MainCategory"),
                "product_name": item.get("ProductName"),
                "review_score": item.get("ReviewScore"),
            }
        )

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            dataset,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"saved: {OUTPUT_PATH}")
    print(f"dataset size: {len(dataset)}")


if __name__ == "__main__":
    main()