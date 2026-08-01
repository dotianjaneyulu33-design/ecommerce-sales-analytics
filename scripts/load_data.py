"""
Day 25 - Load cleaned data into PostgreSQL.
Requires: pip install psycopg2-binary pandas

Run this from the scripts/ folder after updating DB_CONFIG below
with your actual PostgreSQL password.
"""
import psycopg2
import pandas as pd
import warnings
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

# ---------- UPDATE THIS with your real PostgreSQL password ----------
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "project_DB",
    "user": "postgres",
    "password": "anji@4419",
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def seed_lookup_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM platform;")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO platform (name) VALUES ('Amazon'), ('Flipkart');")
        print("Seeded platform table")

    cur.execute("SELECT COUNT(*) FROM category;")
    if cur.fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO category (name) VALUES
            ('Electronics'), ('Fashion'), ('Home & Kitchen'),
            ('Beauty & Personal Care'), ('Automotive'), ('Toys & Baby'),
            ('Office & Stationery'), ('Sports & Fitness'), ('Other');
        """)
        print("Seeded category table")
    conn.commit()
    cur.close()

def get_lookup_maps(conn):
    platform_map = pd.read_sql("SELECT platform_id, name FROM platform", conn).set_index("name")["platform_id"].to_dict()
    category_map = pd.read_sql("SELECT category_id, name FROM category", conn).set_index("name")["category_id"].to_dict()
    return platform_map, category_map

def load_products(conn):
    df = pd.read_csv("../database/clean-data/products_final.csv")
    platform_map, category_map = get_lookup_maps(conn)

    df["platform_id"] = df["platform"].map(platform_map)
    df["category_id"] = df["category"].map(category_map)

    # Drop rows that failed to map (shouldn't happen, but safety check)
    unmapped = df[df["platform_id"].isna() | df["category_id"].isna()]
    if len(unmapped) > 0:
        print(f"WARNING: {len(unmapped)} rows failed to map platform/category — skipping them")
        df = df.dropna(subset=["platform_id", "category_id"])

    cur = conn.cursor()
    rows = df[["id", "platform_id", "category_id", "product_name", "price", "mrp",
               "discount_pct", "rating", "rating_count", "brand", "image_url", "source_url"]].values.tolist()

    # Convert NaN to None for proper NULL insertion
    rows = [[None if pd.isna(v) else v for v in row] for row in rows]

    cur.executemany("""
        INSERT INTO product (id, platform_id, category_id, product_name, price, mrp,
                              discount_pct, rating, rating_count, brand, image_url, source_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, rows)
    conn.commit()
    cur.close()
    print(f"Loaded {len(rows)} products")

def load_reviews(conn):
    df = pd.read_csv("../database/clean-data/reviews_final.csv")

    # reviews_final.csv's product_id is the ORIGINAL Amazon ASIN (e.g. B07JW9H4J1),
    # but the DB's product.id column stores the NEW short uuid generated in Day 14.
    # products_final.csv has both columns, so use it as the bridge:
    #   original product_id (ASIN) -> new short id (uuid) -> product_pk (DB)
    bridge = pd.read_csv("../database/clean-data/products_final.csv")[["product_id", "id"]]
    bridge_map = bridge.set_index("product_id")["id"].to_dict()  # ASIN -> short uuid

    prod_map = pd.read_sql("SELECT product_pk, id FROM product", conn).set_index("id")["product_pk"].to_dict()  # short uuid -> product_pk

    df["short_id"] = df["product_id"].map(bridge_map)
    df["product_pk"] = df["short_id"].map(prod_map)
    unmapped = df[df["product_pk"].isna()]
    if len(unmapped) > 0:
        print(f"WARNING: {len(unmapped)} reviews reference unknown product_id — skipping")
        df = df.dropna(subset=["product_pk"])

    cur = conn.cursor()
    rows = df[["product_pk", "reviewer_id", "reviewer_name", "review_id", "review_title", "review_content"]].values.tolist()
    rows = [[None if pd.isna(v) else v for v in row] for row in rows]

    cur.executemany("""
        INSERT INTO review (product_pk, reviewer_id, reviewer_name, review_title, review_content)
        VALUES (%s, %s, %s, %s, %s);
    """, [[r[0], r[1], r[2], r[4], r[5]] for r in rows])  # skip review_id (col index 3), not in schema
    conn.commit()
    cur.close()
    print(f"Loaded {len(rows)} reviews")

def load_sales(conn):
    """Generate one synthetic sale per product using order_date + random quantity."""
    import numpy as np
    np.random.seed(42)

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sales;")
    if cur.fetchone()[0] > 0:
        print("Sales table already has data — skipping to avoid duplicates")
        cur.close()
        return
    cur.close()

    df = pd.read_csv("../database/clean-data/products_final.csv")
    prod_map = pd.read_sql("SELECT product_pk, id FROM product", conn).set_index("id")["product_pk"].to_dict()
    df["product_pk"] = df["id"].map(prod_map)
    df = df.dropna(subset=["product_pk"])

    df["quantity"] = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                        size=len(df), p=[.30,.20,.15,.10,.08,.07,.04,.03,.02,.01])
    df["revenue"] = (df["price"] * df["quantity"]).round(2)

    cur = conn.cursor()
    rows = df[["product_pk", "order_date", "quantity", "revenue"]].values.tolist()
    cur.executemany("""
        INSERT INTO sales (product_pk, order_date, quantity, revenue)
        VALUES (%s, %s, %s, %s);
    """, rows)
    conn.commit()
    cur.close()
    print(f"Loaded {len(rows)} sales records")

def verify(conn):
    cur = conn.cursor()
    for table in ["platform", "category", "product", "review", "sales"]:
        cur.execute(f"SELECT COUNT(*) FROM {table};")
        print(f"{table}: {cur.fetchone()[0]} rows")
    cur.close()

if __name__ == "__main__":
    conn = get_connection()
    print("Connected to PostgreSQL")

    seed_lookup_tables(conn)
    load_products(conn)
    load_reviews(conn)
    load_sales(conn)

    print("\n--- Final row counts ---")
    verify(conn)

    conn.close()
