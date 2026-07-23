"""
Day 12 - Clean Amazon dataset
Input:  amazon.csv
Output: amazon_clean.csv        (one row per product)
        amazon_reviews_clean.csv (one row per review, exploded)
"""
import pandas as pd
import numpy as np
import re

df = pd.read_csv("amazon.csv")
print(f"Loaded {len(df)} raw rows")

# ---------- 1. Remove duplicate products ----------
before = len(df)
df = df.drop_duplicates(subset="product_id", keep="first").reset_index(drop=True)
print(f"Dropped {before - len(df)} duplicate product_id rows -> {len(df)} rows remain")

# ---------- 2. Clean price / percentage / count fields ----------
def clean_currency(val):
    if pd.isna(val):
        return np.nan
    return float(str(val).replace("₹", "").replace(",", "").strip())

def clean_percentage(val):
    if pd.isna(val):
        return np.nan
    return float(str(val).replace("%", "").strip())

def clean_int_with_commas(val):
    if pd.isna(val):
        return np.nan
    return int(str(val).replace(",", "").strip())

df["discounted_price"] = df["discounted_price"].apply(clean_currency)
df["actual_price"] = df["actual_price"].apply(clean_currency)
df["discount_percentage"] = df["discount_percentage"].apply(clean_percentage)
df["rating_count"] = df["rating_count"].apply(clean_int_with_commas)

# ---------- 3. Fix rating column ----------
def clean_rating(val):
    try:
        f = float(val)
        if 0 <= f <= 5:
            return f
        return np.nan
    except (ValueError, TypeError):
        return np.nan

df["rating"] = df["rating"].apply(clean_rating)
category_avg_rating = df.groupby(df["category"].str.split("|").str[0])["rating"].transform("mean")
df["rating"] = df["rating"].fillna(category_avg_rating)
df["rating"] = df["rating"].fillna(df["rating"].mean())  # final fallback

# ---------- 4. Impute missing rating_count ----------
df["rating_count"] = df["rating_count"].fillna(0).astype(int)

# ---------- 5. Extract top-level category ----------
df["top_category"] = df["category"].str.split("|").str[0].str.strip()

# ---------- 6. Add platform column ----------
df["platform"] = "Amazon"

# ---------- 7. Save cleaned product-level dataset ----------
product_cols = [
    "product_id", "product_name", "top_category", "category",
    "platform", "discounted_price", "actual_price", "discount_percentage",
    "rating", "rating_count", "about_product", "img_link", "product_link"
]
df[product_cols].to_csv("amazon_clean.csv", index=False)
print(f"Saved amazon_clean.csv with {len(df)} rows")

# ---------- 8. Explode bundled reviews into individual rows ----------
review_rows = []
for _, row in df.iterrows():
    # Split each list column on comma; guard against NaN and uneven splits
    def split_list(field):
        val = row.get(field)
        if pd.isna(val):
            return []
        return [x.strip() for x in str(val).split(",")]

    user_ids = split_list("user_id")
    user_names = split_list("user_name")
    review_ids = split_list("review_id")
    titles = split_list("review_title")
    contents = split_list("review_content")

    n = max(len(user_ids), len(user_names), len(review_ids), len(titles), len(contents), 1)

    def get(lst, i):
        return lst[i] if i < len(lst) else None

    for i in range(n):
        review_rows.append({
            "product_id": row["product_id"],
            "reviewer_id": get(user_ids, i),
            "reviewer_name": get(user_names, i),
            "review_id": get(review_ids, i),
            "review_title": get(titles, i),
            "review_content": get(contents, i),
        })

reviews_df = pd.DataFrame(review_rows)
reviews_df.to_csv("amazon_reviews_clean.csv", index=False)
print(f"Saved amazon_reviews_clean.csv with {len(reviews_df)} exploded review rows")

# ---------- Summary ----------
print("\n--- Amazon cleaning summary ---")
print(f"Products: {before} raw -> {len(df)} clean")
print(f"Reviews exploded: {len(reviews_df)} rows")
print(f"Remaining nulls in clean product data:\n{df[product_cols].isna().sum()[df[product_cols].isna().sum() > 0]}")
