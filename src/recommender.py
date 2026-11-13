
import pandas as pd
import math

# Load engineered product features
products = pd.read_csv("outputs/product_features.csv")

# Keep product IDs separate from the feature values
product_ids = products["product_id"]
features = products.drop(columns=["product_id"])

# Calculate cosine similarity without scikit-learn
def cosine_similarity(row_a, row_b):
    dot_product = sum(a * b for a, b in zip(row_a, row_b))
    magnitude_a = math.sqrt(sum(a * a for a in row_a))
    magnitude_b = math.sqrt(sum(b * b for b in row_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)


def recommend_products(product_id, number_of_recommendations=5):
    if product_id not in product_ids.values:
        print(f"Product ID {product_id} was not found.")
        return

    selected_index = product_ids[product_ids == product_id].index[0]
    selected_features = features.iloc[selected_index].tolist()

    scores = []

    for index, row in features.iterrows():
        if index == selected_index:
            continue

        score = cosine_similarity(
            selected_features,
            row.tolist()
        )

        scores.append((product_ids.iloc[index], score))

    scores.sort(key=lambda item: item[1], reverse=True)

    print(f"\nRecommendations for product ID {product_id}:")
    for recommended_id, score in scores[:number_of_recommendations]:
        print(f"Product ID: {recommended_id} | Similarity: {score:.3f}")


if __name__ == "__main__":
    first_product_id = product_ids.iloc[0]
    recommend_products(first_product_id)




