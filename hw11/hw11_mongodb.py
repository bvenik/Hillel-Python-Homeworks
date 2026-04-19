import pymongo
from datetime import datetime, timedelta

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["online_shop"]
products_col = db["products"]
orders_col = db["orders"]

sample_products = [
    {"name": "Миша", "price": 1200, "category": "Периферія", "stock": 10, "available": True},
    {"name": "Клавіатура", "price": 2500, "category": "Периферія", "stock": 5, "available": True},
    {"name": "Монітор", "price": 8000, "category": "Електроніка", "stock": 0, "available": False},
    {"name": "Навушники", "price": 1500, "category": "Периферія", "stock": 7, "available": True}
]
products_col.insert_many(sample_products)

orders = [
    {
        "order_num": 101,
        "customer": "Володя",
        "items": [{"product": "Миша", "quantity": 1}],
        "total_sum": 1200,
        "date": datetime.now()
    },
    {
        "order_num": 102,
        "customer": "Володя",
        "items": [{"product": "Клавіатура", "quantity": 1}],
        "total_sum": 2500,
        "date": datetime.now()
    },
    {
        "order_num": 103,
        "customer": "Петро",
        "items": [{"product": "Навушники", "quantity": 1}],
        "total_sum": 1500,
        "date": datetime.now()
    }
]
orders_col.insert_many(orders)

thirty_days_ago = datetime.now() - timedelta(days=30)
recent_orders = orders_col.find({"date": {"$gte": thirty_days_ago}})

print("--- Замовлення за останні 30 днів ---")
for i in recent_orders:
    print(f"Замовлення №{i['order_num']} від {i['date']} (Клієнт: {i['customer']} {i['total_sum']} грн)")

products_col.update_one(
    {"name": "Миша"},
    {"$inc": {"stock": -1}}
)
products_col.delete_many({"stock": {"$lte": 0}})

pipeline_volodya = [
    {"$match": {"customer": "Володя"}},
    {"$group": {
        "_id": "$customer",
        "total_spent": {"$sum": "$total_sum"}
    }}
]

pipeline_all = [
    {"$group": {
        "_id": "$customer",
        "total_spent": {"$sum": "$total_sum"}
    }}
]

print("\n--- Результати агрегації, замовлення на ім'я Володя ---")
for result in orders_col.aggregate(pipeline_volodya):
    print(f"Клієнт {result['_id']} витратив {result['total_spent']} грн")

print("\n--- Загальний звіт по всіх клієнтах ---")
for result in orders_col.aggregate(pipeline_all):
    print(f"Клієнт {result['_id']} сумарно витратив {result['total_spent']} грн")

products_col.create_index([("category", 1)])
print("\nІндекс для поля 'category' успішно створено.")
