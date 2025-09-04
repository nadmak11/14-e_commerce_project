import sqlite3
import json
from pathlib import Path

# ИЗМЕНЕНИЕ ЗДЕСЬ:
DATA_DIR = Path(__file__).parent / "data"
DB_FILE = DATA_DIR / "shop.db"
CONFIG_FILE = Path(__file__).parent / "config.json"

# --- Создаем таблицы ---
# Удаляем старый файл БД, если он существует, для чистого старта
DB_FILE.unlink(missing_ok=True)

# Подключаемся к БД (она будет создана, если не существует)
con = sqlite3.connect(DB_FILE)
cur = con.cursor()

# Создаем таблицу товаров
cur.execute(
    """
    CREATE TABLE products (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL
    )
"""
)

# Создаем таблицу склада
cur.execute(
    """
    CREATE TABLE inventory (
        product_id TEXT PRIMARY KEY,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
"""
)

print("Таблицы 'products' и 'inventory' успешно созданы.")

# --- Наполняем таблицы данными из config.json ---
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Наполняем таблицу товаров
products_to_insert = [
    (pid, pdata["name"], pdata["price"]) for pid, pdata in data["products"].items()
]
cur.executemany("INSERT INTO products VALUES (?, ?, ?)", products_to_insert)
print(f"Добавлено {len(products_to_insert)} товаров в таблицу 'products'.")

# Наполняем таблицу склада
inventory_to_insert = [(pid, qty) for pid, qty in data["inventory"].items()]
cur.executemany("INSERT INTO inventory VALUES (?, ?)", inventory_to_insert)
print(f"Добавлено {len(inventory_to_insert)} записей в таблицу 'inventory'.")

# Сохраняем изменения и закрываем соединение
con.commit()
con.close()

print(f"База данных '{DB_FILE.name}' успешно создана и наполнена данными.")
