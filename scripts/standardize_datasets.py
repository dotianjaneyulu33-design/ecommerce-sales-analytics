"""
Day 13 - Standardize category names and dates across both datasets.
Input:  amazon_clean.csv, flipkart_clean.csv
Output: amazon_standardized.csv, flipkart_standardized.csv
"""
import pandas as pd
import numpy as np

np.random.seed(42)  # reproducible synthetic dates

amz = pd.read_csv("clean_data/amazon_clean.csv")
fk = pd.read_csv("clean_data/flipkart_clean.csv")

# ---------- Shared category taxonomy ----------
# Maps every raw top_category value (from either platform) onto one of 8
# standard categories used throughout the rest of the project.
CATEGORY_MAP = {
    # Amazon raw -> standard
    "Electronics": "Electronics",
    "Computers&Accessories": "Electronics",
    "OfficeProducts": "Office & Stationery",
    "Home&Kitchen": "Home & Kitchen",
    "HomeImprovement": "Home & Kitchen",
    "MusicalInstruments": "Other",
    "Toys&Games": "Toys & Baby",
    "Car&Motorbike": "Automotive",
    "Health&PersonalCare": "Beauty & Personal Care",

    # Flipkart raw -> standard
    "Clothing": "Fashion",
    "Jewellery": "Fashion",
    "Footwear": "Fashion",
    "Bags, Wallets & Belts": "Fashion",
    "Watches": "Fashion",
    "Mobiles & Accessories": "Electronics",
    "Computers": "Electronics",
    "Cameras & Accessories": "Electronics",
    "Automotive": "Automotive",
    "Home Decor & Festive Needs": "Home & Kitchen",
    "Home Furnishing": "Home & Kitchen",
    "Kitchen & Dining": "Home & Kitchen",
    "Furniture": "Home & Kitchen",
    "Tools & Hardware": "Home & Kitchen",
    "Home Improvement": "Home & Kitchen",
    "Beauty and Personal Care": "Beauty & Personal Care",
    "Baby Care": "Toys & Baby",
    "Toys & School Supplies": "Toys & Baby",
    "Pens & Stationery": "Office & Stationery",
    "Sports & Fitness": "Sports & Fitness",
}

def map_category(raw):
    return CATEGORY_MAP.get(raw, "Other")

amz["standard_category"] = amz["top_category"].apply(map_category)
fk["standard_category"] = fk["top_category"].apply(map_category)

print("Amazon -> standard_category distribution:")
print(amz["standard_category"].value_counts())
print("\nFlipkart -> standard_category distribution:")
print(fk["standard_category"].value_counts())

# ---------- Synthetic order dates ----------
# Neither dataset has real transaction dates. We generate a plausible
# order date per product within a fixed 2-year window (2024-01-01 to
# 2025-12-31), documented as SYNTHETIC in the data dictionary.
date_start = pd.Timestamp("2024-01-01")
date_end = pd.Timestamp("2025-12-31")
date_range_days = (date_end - date_start).days

def random_date():
    offset = np.random.randint(0, date_range_days)
    return date_start + pd.Timedelta(days=offset)

amz["order_date"] = [random_date() for _ in range(len(amz))]
fk["order_date"] = [random_date() for _ in range(len(fk))]

amz["order_date"] = amz["order_date"].dt.strftime("%Y-%m-%d")
fk["order_date"] = fk["order_date"].dt.strftime("%Y-%m-%d")

# ---------- Standardize price precision ----------
amz["discounted_price"] = amz["discounted_price"].round(2)
amz["actual_price"] = amz["actual_price"].round(2)
fk["discounted_price"] = fk["discounted_price"].round(2)
fk["retail_price"] = fk["retail_price"].round(2)

# ---------- Save ----------
amz.to_csv("clean_data/amazon_standardized.csv", index=False)
fk.to_csv("clean_data/flipkart_standardized.csv", index=False)
print(f"\nSaved amazon_standardized.csv ({len(amz)} rows)")
print(f"Saved flipkart_standardized.csv ({len(fk)} rows)")
