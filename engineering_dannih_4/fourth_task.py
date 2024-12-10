import msgpack
import json
from common import connect_to_db

msgpack_file = "data/4/_product_data.msgpack"
json_file = "data/4/_update_data.json"
db_path = "product_data.db"

def load_msgpack(file):
    with open(file, "rb") as f:
        return msgpack.unpack(f, raw=False)

def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def create_product_table(db):
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            price FLOAT,
            quantity INTEGER,
            category TEXT,
            fromCity TEXT,
            isAvailable BOOLEAN,
            views INTEGER,
            update_count INTEGER DEFAULT 0
        )
    """)
    db.commit()

def insert_products(db, products):
    cursor = db.cursor()
    for product in products:
        cursor.execute("""
            INSERT OR IGNORE INTO product_data (name, price, quantity, category, fromCity, isAvailable, views)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product["name"], 
            product["price"], 
            product["quantity"], 
            product["category"], 
            product["fromCity"], 
            product["isAvailable"], 
            product["views"]
        ))
    db.commit()

def apply_updates(db, updates):
    cursor = db.cursor()
    for update in updates:
        name = update["name"]
        method = update["method"]
        param = update["param"]

        cursor.execute("SELECT * FROM product_data WHERE name = ?", (name,))
        product = cursor.fetchone()
        if not product:
            continue

        if method == "price_percent":
            new_price = product["price"] + product["price"] * param
            if new_price < 0:
                continue
            cursor.execute("UPDATE product_data SET price = ?, update_count = update_count + 1 WHERE name = ?", (new_price, name))
        
        elif method == "price_abs":
            new_price = product["price"] + param
            if new_price < 0:
                continue
            cursor.execute("UPDATE product_data SET price = ?, update_count = update_count + 1 WHERE name = ?", (new_price, name))
        
        elif method == "quantity_add":
            new_quantity = product["quantity"] + param
            if new_quantity < 0:
                continue
            cursor.execute("UPDATE product_data SET quantity = ?, update_count = update_count + 1 WHERE name = ?", (new_quantity, name))
        
        elif method == "quantity_sub":
            new_quantity = product["quantity"] + param  
            if new_quantity < 0:
                continue
            cursor.execute("UPDATE product_data SET quantity = ?, update_count = update_count + 1 WHERE name = ?", (new_quantity, name))
        
        elif method == "remove":
            cursor.execute("DELETE FROM product_data WHERE name = ?", (name,))

    db.commit()

def execute_queries(db):
    cursor = db.cursor()

    cursor.execute("""
        SELECT name, update_count 
        FROM product_data
        ORDER BY update_count DESC
        LIMIT 10
    """)
    top_updated = [dict(row) for row in cursor.fetchall()]
    print("Топ-10 самых обновляемых товаров:")
    for item in top_updated:
        print(item)

    cursor.execute("""
        SELECT category, 
               SUM(price) as total_price, 
               MIN(price) as min_price, 
               MAX(price) as max_price, 
               ROUND(AVG(price), 2) as avg_price, 
               COUNT(*) as item_count
        FROM product_data
        GROUP BY category
    """)
    price_analysis = [dict(row) for row in cursor.fetchall()]
    print("\nАнализ цен:")
    for item in price_analysis:
        print(item)

    cursor.execute("""
        SELECT category, 
               SUM(quantity) as total_quantity, 
               MIN(quantity) as min_quantity, 
               MAX(quantity) as max_quantity, 
               ROUND(AVG(quantity), 2) as avg_quantity
        FROM product_data
        GROUP BY category
    """)
    stock_analysis = [dict(row) for row in cursor.fetchall()]
    print("\nАнализ остатков:")
    for item in stock_analysis:
        print(item)

    cursor.execute("""
        SELECT * 
        FROM product_data 
        WHERE quantity > 100
    """)
    items_with_high_quantity = [dict(row) for row in cursor.fetchall()]
    print("\nТовары с количеством больше 100:")
    for item in items_with_high_quantity:
        print(item)
        
db = connect_to_db(db_path)
create_product_table(db)

msgpack_data = load_msgpack(msgpack_file)
json_data = load_json(json_file)

products = [{
    "name": item.get("name", ""), 
    "price": item.get("price", 0.0), 
    "quantity": item.get("quantity", 0), 
    "category": item.get("category", ""), 
    "fromCity": item.get("fromCity", ""), 
    "isAvailable": bool(item.get("isAvailable", 0)), 
    "views": item.get("views", 0)
} for item in msgpack_data]

insert_products(db, products)

apply_updates(db, json_data)

execute_queries(db)
