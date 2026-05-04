import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('online_shop.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    category TEXT,
    stock INTEGER,
    available BOOLEAN
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_num INTEGER,
    customer TEXT,
    total_sum REAL,
    date TEXT
)''')

sample_products = [
    ('Миша', 1200, 'Периферія', 10, 1),
    ('Клавіатура', 2500, 'Периферія', 5, 1),
    ('Монітор', 8000, 'Електроніка', 0, 0),
    ('Навушники', 1500, 'Периферія', 7, 1)
]
cursor.executemany("INSERT INTO products (name, price, category, stock, available) VALUES (?, ?, ?, ?, ?)", sample_products)

orders = [
    (101, 'Володя', 1200, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    (102, 'Володя', 2500, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    (103, 'Петро', 1500, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
]
cursor.executemany("INSERT INTO orders (order_num, customer, total_sum, date) VALUES (?, ?, ?, ?)", orders)

thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
cursor.execute("SELECT order_num, date, customer, total_sum FROM orders WHERE date >= ?", (thirty_days_ago,))

print("--- SQL: Замовлення за останні 30 днів ---")
for row in cursor.fetchall():
    print(f"Замовлення №{row[0]} від {row[1]} (Клієнт: {row[2]} {row[3]} грн)")

cursor.execute("UPDATE products SET stock = stock - 1 WHERE name = 'Миша'")

cursor.execute("DELETE FROM products WHERE stock <= 0")

print("\n--- SQL: Результати агрегації (Звіт по всіх клієнтах) ---")
cursor.execute("SELECT customer, SUM(total_sum) FROM orders GROUP BY customer")
for row in cursor.fetchall():
    print(f"Клієнт {row[0]} сумарно витратив {row[1]} грн")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON products(category)")

conn.commit()
conn.close()
print("\nSQL операції завершені!")