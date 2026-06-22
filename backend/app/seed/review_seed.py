import json
import random

from app.models.review import Review


def seed_reviews(db):

    with open(
        "app/ml/data/fashion_training_dataset.json",
        encoding="utf-8",
    ) as f:
        data = json.load(f)

    samples = random.sample(
        data,
        5000,
    )

    for item in samples:

        review = Review(
            product_id=random.randint(1, 5),
            rating=random.randint(1, 5),
            content=item["text"],
            sentiment=item["sentiment"],
            tags=",".join(item["tags"]),
        )

        db.add(review)

    db.commit()

    print(f"{len(samples)} reviews seeded")