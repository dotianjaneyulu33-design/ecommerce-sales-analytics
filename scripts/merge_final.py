"""
Day 14 - Merge Amazon and Flipkart into final, load-ready datasets.
Input:  amazon_standardized.csv, flipkart_standardized.csv, amazon_reviews_clean.csv
Output: products_final.csv   (unified Product table, both platforms)
        reviews_final.csv    (unified Review table, Amazon only - Flipkart has no review text)
"""
import pandas as pd
import uuid

amz = pd.read_csv("clean_data/amazon_standardized.csv")
fk = pd.read_csv("clean_data/flipkart_standardized.csv")

# ---------- Build unified Product schema ----------
# Common columns both platforms will share in the final Product table:
# product_id, platform, product_name, category, price, mrp, discount_pct,
# rating, rating_count, brand, order_date, image_url, source_url

amz_final = pd.DataFrame({
    "product_id": amz["product_id"],
    "platform": amz["platform"],
    "product_name": amz["product_name"],
    "category": amz["standard_category"],
    "price": amz["discounted_price"],
    "mrp": amz["actual_price"],
    "discount_pct": amz["discount_percentage"],
    "rating": amz["rating"],
    "rating_count": amz["rating_count"],
    "brand": None,  # Amazon dataset has no brand column
    "order_date": amz["order_date"],
    "image_url": amz["img_link"],
    "source_url": amz["product_link"],
})

fk_final = pd.DataFrame({
    "product_id": fk["uniq_id"],
    "platform": fk["platform"],
    "product_name": fk["product_name"],
    "category": fk["standard_category"],
    "price": fk["discounted_price"],
    "mrp": fk["retail_price"],
    "discount_pct": fk["discount_percentage"],
    "rating": fk["rating"],
    "rating_count": None,  # Flipkart dataset has no rating_count column
    "brand": fk["brand"],
    "order_date": fk["order_date"],
    "image_url": fk["image_url"],
    "source_url": fk["product_url"],
})

products_final = pd.concat([amz_final, fk_final], ignore_index=True)

# Add a surrogate primary key (since Amazon/Flipkart IDs could theoretically collide)
products_final.insert(0, "id", [str(uuid.uuid4())[:8] for _ in range(len(products_final))])

products_final.to_csv("clean_data/products_final.csv", index=False)
print(f"Saved products_final.csv: {len(products_final)} rows")
print(f"  Amazon: {(products_final['platform']=='Amazon').sum()}")
print(f"  Flipkart: {(products_final['platform']=='Flipkart').sum()}")

# ---------- Reviews (Amazon only - Flipkart has no review text) ----------
reviews = pd.read_csv("clean_data/amazon_reviews_clean.csv")
reviews.insert(0, "id", [str(uuid.uuid4())[:8] for _ in range(len(reviews))])
reviews["platform"] = "Amazon"
reviews.to_csv("clean_data/reviews_final.csv", index=False)
print(f"\nSaved reviews_final.csv: {len(reviews)} rows (Amazon only)")

# ---------- Quick sanity summary ----------
print("\n--- Final dataset summary ---")
print(f"Total products (both platforms): {len(products_final)}")
print(f"Total reviews: {len(reviews)}")
print(f"\nCategory distribution in final product table:")
print(products_final.groupby(["category","platform"]).size().unstack(fill_value=0))
