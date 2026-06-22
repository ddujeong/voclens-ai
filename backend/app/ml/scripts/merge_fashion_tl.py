import json
from pathlib import Path


BASE_DIR = Path(__file__).parents[1] / "data" / "tl"
OUTPUT_PATH = Path(__file__).parents[1] / "data" / "fashion_labeled_reviews.json"

CATEGORY_DIRS = [
    "women",
    "men",
    "shoes",
    "goods",
]


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    all_reviews = []

    for category_dir in CATEGORY_DIRS:
        folder = BASE_DIR / category_dir
        json_files = sorted(folder.glob("*.json"))

        print(f"{category_dir}: {len(json_files)} files")

        for file_path in json_files:
            data = load_json(file_path)

            if isinstance(data, list):
                all_reviews.extend(data)
            else:
                all_reviews.append(data)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            all_reviews,
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"merged reviews: {len(all_reviews)}")
    print(f"saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()