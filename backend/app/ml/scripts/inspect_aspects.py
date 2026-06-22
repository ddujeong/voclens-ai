import json
from collections import Counter
from pathlib import Path

DATA_PATH = Path(__file__).parents[1] / "data" / "fashion_labeled_reviews.json"

with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

aspect_counter = Counter()
polarity_counter = Counter()

for item in data:
    for aspect in item.get("Aspects", []):
        aspect_name = aspect["Aspect"]
        polarity = aspect["SentimentPolarity"]

        aspect_counter[aspect_name] += 1
        polarity_counter[polarity] += 1

print("총 리뷰 수:", len(data))
print("\nAspect TOP 30")
for aspect, count in aspect_counter.most_common(30):
    print(aspect, count)

print("\nPolarity")
for polarity, count in polarity_counter.items():
    print(polarity, count)