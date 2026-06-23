import json
import random

from app.models.review import Review
from app.models.product import Product


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

    product_map = {}

    for item in samples:
        product_name = item.get("product_name")
        category = item.get("category")

        if not product_name or not category:
            continue

        product_key = (
            category,
            product_name,
        )

        if product_key not in product_map:
            product = Product(
                name=product_name,
                brand="AI-Hub",
                category=category,
                price=0,
            )

            db.add(product)
            db.flush()

            product_map[product_key] = product.id

        review = Review(
            product_id=product_map[product_key],
            rating=random.randint(1, 5),
            content=item["text"],
            sentiment=item["sentiment"],
            tags=",".join(item["tags"]),
        )

        db.add(review)

    db.commit()

    print(f"{len(samples)} reviews seeded")
    print(f"{len(product_map)} products seeded")