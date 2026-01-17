from __future__ import annotations

import os
import random
import sqlite3
from datetime import date, timedelta

DB_PATH = os.getenv("DB_PATH", "data/ecommerce.db")


SCHEMA = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price REAL NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL,
  status TEXT NOT NULL,
  order_date TEXT NOT NULL,
  FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price REAL NOT NULL,
  FOREIGN KEY(order_id) REFERENCES orders(id),
  FOREIGN KEY(product_id) REFERENCES products(id)
);
"""


CUSTOMERS = [
    "Maria Petrova", "Ivan Ivanov", "Elena Dimitrova", "Georgi Nikolov",
    "Alex Stoyanov", "Viktoria Hristova", "Daniel Marinov", "Nikol Stoyanova"
]
CATEGORIES = ["Electronics", "Home", "Sports", "Books", "Beauty"]
PRODUCTS = [
    ("Wireless Headphones", "Electronics", 120.00),
    ("Mechanical Keyboard", "Electronics", 90.00),
    ("Coffee Maker", "Home", 75.00),
    ("Vacuum Cleaner", "Home", 140.00),
    ("Yoga Mat", "Sports", 25.00),
    ("Dumbbells Set", "Sports", 60.00),
    ("Novel Book", "Books", 15.00),
    ("Skincare Set", "Beauty", 35.00),
]


def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def main() -> None:
    random.seed(42)
    ensure_dir(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SCHEMA)

        conn.executemany("INSERT INTO customers(full_name) VALUES (?)", [(c,) for c in CUSTOMERS])
        conn.executemany("INSERT INTO products(name, category, price) VALUES (?, ?, ?)", PRODUCTS)

        customer_ids = [r[0] for r in conn.execute("SELECT id FROM customers").fetchall()]
        product_rows = conn.execute("SELECT id, price FROM products").fetchall()
        products = [(r[0], r[1]) for r in product_rows]

        statuses = ["paid", "shipped", "delivered", "cancelled"]
        start = date.today() - timedelta(days=365)

        # Create orders + items
        for _ in range(120):
            cust_id = random.choice(customer_ids)
            status = random.choices(statuses, weights=[35, 25, 30, 10], k=1)[0]
            od = (start + timedelta(days=random.randint(0, 365))).isoformat()

            cur = conn.execute(
                "INSERT INTO orders(customer_id, status, order_date) VALUES (?, ?, ?)",
                (cust_id, status, od),
            )
            order_id = cur.lastrowid

            # 1-4 items
            for _ in range(random.randint(1, 4)):
                product_id, base_price = random.choice(products)
                qty = random.randint(1, 3)
                unit_price = round(base_price * random.uniform(0.95, 1.05), 2)
                conn.execute(
                    "INSERT INTO order_items(order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                    (order_id, product_id, qty, unit_price),
                )

        conn.commit()
        print(f"Seeded DB: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
