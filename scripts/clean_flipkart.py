"""
Day 12 - Clean Flipkart dataset
Input:  flipkart.csv
Output: flipkart_clean.csv
"""
import pandas as pd
import numpy as np
import re

df = pd.read_csv("flipkart.csv")
print(f"Loaded {len(df)} raw rows")

# ---------- 1. Duplicates ----------
before = len(df)
df = df.drop_duplicates(subset="uniq_id", keep="first").reset_index(drop=True)
print(f"Dropped {before - len(df)} duplicate uniq_id rows (expected 0)")

# ---------- 2. Handle missing prices: exclude rows missing both ----------
before_price = len(df)
df = df.dropna(subset=["retail_price", "discounted_price"]).reset_index(drop=True)
print(f"Dropped {before_price - len(df)} rows with missing price data -> {len(df)} rows remain")

# ---------- 3. Clean ratings: "No rating available" -> NaN ----------
def clean_rating(val):
    try:
        f = float(val)
        if 0 <= f <= 5:
            return f
        return np.nan
    except (ValueError, TypeError):
        return np.nan

df["product_rating"] = df["product_rating"].apply(clean_rating)
df["overall_rating"] = df["overall_rating"].apply(clean_rating)
# Use product_rating, fall back to overall_rating, else leave NULL (do NOT impute - true "unrated" state)
df["rating"] = df["product_rating"].fillna(df["overall_rating"])

# ---------- 4. Brand: keep NULL as "Unknown" flag column, don't fabricate ----------
df["brand"] = df["brand"].fillna("Unknown")

# ---------- 5. Extract top-level category ----------
def extract_top_category(val):
    if pd.isna(val):
        return "Unknown"
    cleaned = re.sub(r'^\["|"\]$', '', str(val))
    return cleaned.split(">>")[0].strip()

df["top_category"] = df["product_category_tree"].apply(extract_top_category)

# ---------- 6. Discount percentage (derived, doesn't exist in raw file) ----------
df["discount_percentage"] = ((df["retail_price"] - df["discounted_price"]) / df["retail_price"] * 100).round(2)

# ---------- 7. Add platform column ----------
df["platform"] = "Flipkart"

# ---------- 8. Extract first image URL ----------
def first_image(val):
    if pd.isna(val):
        return None
    match = re.search(r'"(http[^"]+)"', str(val))
    return match.group(1) if match else None

df["image_url"] = df["image"].apply(first_image)

# ---------- 9. Save cleaned dataset ----------
product_cols = [
    "uniq_id", "product_name", "top_category", "product_category_tree",
    "platform", "brand", "discounted_price", "retail_price", "discount_percentage",
    "rating", "description", "image_url", "product_url"
]
df[product_cols].to_csv("flipkart_clean.csv", index=False)
print(f"Saved flipkart_clean.csv with {len(df)} rows")

# ---------- Summary ----------
print("\n--- Flipkart cleaning summary ---")
print(f"Products: {before} raw -> {len(df)} clean")
rated = df["rating"].notna().sum()
print(f"Products with a real rating: {rated} ({rated/len(df)*100:.1f}%)")
print(f"Products with brand 'Unknown': {(df['brand']=='Unknown').sum()}")
null_counts = df[product_cols].isna().sum()
print(f"\nRemaining nulls (rating is expected to have many - genuinely unrated):\n{null_counts[null_counts > 0]}")
