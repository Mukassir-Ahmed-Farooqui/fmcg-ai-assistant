import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import sqlite3
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# --- Parameters ---
NUM_STORES = 30
WEEKS = 24
START_DATE = datetime(2023, 7, 3) # A Monday

# --- 1. Product Master ---
products_data = [
    {"product_id": "BEV-001", "product_name": "Spark Lemon Sparkling Water 500ml", "brand": "Spark", "category": "Water", "sub_category": "Sparkling Water", "pack_size_ml": 500, "unit_price": 1.50},
    {"product_id": "BEV-002", "product_name": "Spark Berry Sparkling Water 500ml", "brand": "Spark", "category": "Water", "sub_category": "Sparkling Water", "pack_size_ml": 500, "unit_price": 1.50},
    {"product_id": "BEV-003", "product_name": "AquaPure Still Water 1L", "brand": "AquaPure", "category": "Water", "sub_category": "Still Water", "pack_size_ml": 1000, "unit_price": 1.20},
    {"product_id": "BEV-004", "product_name": "Fizzy Cola Classic 330ml", "brand": "Fizzy", "category": "Carbonated", "sub_category": "Cola", "pack_size_ml": 330, "unit_price": 1.00},
    {"product_id": "BEV-005", "product_name": "Fizzy Cola Zero 330ml", "brand": "Fizzy", "category": "Carbonated", "sub_category": "Cola", "pack_size_ml": 330, "unit_price": 1.00},
    {"product_id": "BEV-006", "product_name": "Zest Orange Soda 500ml", "brand": "Zest", "category": "Carbonated", "sub_category": "Fruit Soda", "pack_size_ml": 500, "unit_price": 1.30},
    {"product_id": "BEV-007", "product_name": "Zest Lemon Soda 500ml", "brand": "Zest", "category": "Carbonated", "sub_category": "Fruit Soda", "pack_size_ml": 500, "unit_price": 1.30},
    {"product_id": "BEV-008", "product_name": "Nature's Best Apple Juice 1L", "brand": "Nature's Best", "category": "Juice", "sub_category": "Fruit Juice", "pack_size_ml": 1000, "unit_price": 3.50},
    {"product_id": "BEV-009", "product_name": "Nature's Best Orange Juice 1L", "brand": "Nature's Best", "category": "Juice", "sub_category": "Fruit Juice", "pack_size_ml": 1000, "unit_price": 3.80},
    {"product_id": "BEV-010", "product_name": "Tropical Mix Juice 500ml", "brand": "Nature's Best", "category": "Juice", "sub_category": "Fruit Juice", "pack_size_ml": 500, "unit_price": 2.00},
    {"product_id": "BEV-011", "product_name": "PowerUp Energy Original 250ml", "brand": "PowerUp", "category": "Energy", "sub_category": "Sports Drink", "pack_size_ml": 250, "unit_price": 2.50},
    {"product_id": "BEV-012", "product_name": "PowerUp Energy Sugar-Free 250ml", "brand": "PowerUp", "category": "Energy", "sub_category": "Sports Drink", "pack_size_ml": 250, "unit_price": 2.50},
    {"product_id": "BEV-013", "product_name": "Daily Calcium Milk 1L", "brand": "DailyDairy", "category": "Dairy", "sub_category": "Milk", "pack_size_ml": 1000, "unit_price": 1.80},
    {"product_id": "BEV-014", "product_name": "Choco Delight Milk 500ml", "brand": "DailyDairy", "category": "Dairy", "sub_category": "Flavored Milk", "pack_size_ml": 500, "unit_price": 1.50},
    {"product_id": "BEV-015", "product_name": "Iced Tea Peach 500ml", "brand": "ChillTea", "category": "Tea", "sub_category": "Iced Tea", "pack_size_ml": 500, "unit_price": 1.60},
]
df_products = pd.DataFrame(products_data)

# --- 2. Store Master ---
regions = ["North", "South", "East", "West"]
formats = ["Supermarket", "Hypermarket", "Convenience", "Wholesale"]
cities = {
    "North": ["Manchester", "Leeds", "Newcastle", "Liverpool"],
    "South": ["London", "Brighton", "Southampton", "Bristol"],
    "East": ["Norwich", "Cambridge", "Ipswich", "Peterborough"],
    "West": ["Cardiff", "Swansea", "Newport", "Bath"]
}

stores_data = []
for i in range(1, NUM_STORES + 1):
    region = random.choice(regions)
    city = random.choice(cities[region])
    store_format = np.random.choice(formats, p=[0.4, 0.2, 0.3, 0.1])
    stores_data.append({
        "store_id": f"STR-{i:03d}",
        "store_name": f"{city} {store_format} {i}",
        "region": region,
        "city": city,
        "store_format": store_format
    })
df_stores = pd.DataFrame(stores_data)

# --- 3. Generate Weeks ---
weeks = [(START_DATE + timedelta(weeks=i)).strftime("%Y-%m-%d") for i in range(WEEKS)]

# --- 4. Sales & Promotions / Inventory ---
sales_data = []
inventory_data = []

promotion_types = ["Price Cut", "BOGO", "Display Feature", "Bundle"]

for week in weeks:
    for _, store in df_stores.iterrows():
        for _, product in df_products.iterrows():
            # Base logic
            base_sales = np.random.normal(loc=100, scale=20)
            if product["category"] == "Water":
                base_sales *= 1.5
            if store["store_format"] == "Hypermarket":
                base_sales *= 2.0
            elif store["store_format"] == "Convenience":
                base_sales *= 0.5
                
            # Promotions
            is_promo = random.random() < 0.15 # 15% chance of promo
            promo_type = random.choice(promotion_types) if is_promo else None
            discount_pct = 0.0
            
            if is_promo:
                if promo_type == "Price Cut":
                    discount_pct = random.choice([0.1, 0.2, 0.3])
                elif promo_type == "BOGO":
                    discount_pct = 0.5
                
                # Boost sales heavily if promoted
                sales_multiplier = 1.5 + (discount_pct * 3) + (1.0 if promo_type == "Display Feature" else 0)
                base_sales *= sales_multiplier
            
            units_sold = int(max(0, round(base_sales)))
            
            revenue = units_sold * product["unit_price"] * (1 - discount_pct)
            
            sales_data.append({
                "week_start_date": week,
                "product_id": product["product_id"],
                "store_id": store["store_id"],
                "region": store["region"],
                "units_sold": units_sold,
                "revenue": round(revenue, 2),
                "promotion_flag": is_promo,
                "promotion_type": promo_type,
                "discount_pct": discount_pct
            })
            
            # Inventory logic
            # Simplistic: trying to maintain 1.5x weekly sales as stock
            opening_stock = int(units_sold * random.uniform(0.8, 1.8))
            units_received = int(units_sold * random.uniform(0.5, 1.2))
            
            closing_stock = opening_stock + units_received - units_sold
            stockout_flag = False
            
            if closing_stock < 0:
                units_sold = opening_stock + units_received
                closing_stock = 0
                stockout_flag = True
                
            inventory_data.append({
                "week_start_date": week,
                "product_id": product["product_id"],
                "store_id": store["store_id"],
                "opening_stock": opening_stock,
                "units_received": units_received,
                "units_sold": units_sold,
                "closing_stock": closing_stock,
                "stockout_flag": stockout_flag
            })
            
            # Fix units_sold in sales data in case of stockout
            sales_data[-1]["units_sold"] = units_sold
            sales_data[-1]["revenue"] = round(units_sold * product["unit_price"] * (1 - discount_pct), 2)

df_sales = pd.DataFrame(sales_data)
df_inventory = pd.DataFrame(inventory_data)

# --- Save to DB & CSV ---
os.makedirs("data", exist_ok=True)
df_products.to_csv("data/product_master.csv", index=False)
df_stores.to_csv("data/store_master.csv", index=False)
df_sales.to_csv("data/sales_promotions.csv", index=False)
df_inventory.to_csv("data/inventory.csv", index=False)

conn = sqlite3.connect("fmcg.db")
df_products.to_sql("product_master", conn, if_exists="replace", index=False)
df_stores.to_sql("store_master", conn, if_exists="replace", index=False)
df_sales.to_sql("sales_promotions", conn, if_exists="replace", index=False)
df_inventory.to_sql("inventory", conn, if_exists="replace", index=False)
conn.close()

print("Data generation complete! Saved to data/ and fmcg.db")
