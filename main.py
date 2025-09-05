# Добавлена новая строка для обработки команды pull
import argparse
import sys
import sqlite3
from pathlib import Path
from shop import StoreRepository, OrderService
from shop.exceptions import ShopError


def main():
    parser = argparse.ArgumentParser(
        description="CLI для управления заказами в магазине."
    )
    parser.add_argument("-p", "--product", type=str, required=True, help="ID продукта.")
    parser.add_argument(
        "-q", "--quantity", type=int, required=True, help="Количество товара."
    )
    parser.add_argument("-c", "--currency", type=str, default="RUB", help="Валюта.")
    args = parser.parse_args()

    # --- Сборка приложения ---
    # ИЗМЕНЕНИЕ ЗДЕСЬ:


db_path = Path(__file__).parent / "data" / "shop.db"

if not db_path.exists():
    print(f"Ошибка: Файл базы данных '{db_path.name}' не найден.", file=sys.stderr)
    print(
        "Пожалуйста, запустите скрипт 'database_setup.py' для его создания.",
        file=sys.stderr,
    )
    sys.exit(1)

# 1. Устанавливаем соединение с базой данных
connection = sqlite3.connect(db_path)

try:
    # 2. Создаем репозиторий, передавая ему соединение
    repository = StoreRepository(connection=connection)

    # 3. Создаем сервис
    order_service = OrderService(repository=repository)

    # 4. Вызываем основную логику
    result = order_service.create_order(
        product_id=args.product, quantity=args.quantity, currency=args.currency
    )
    print(result)

except ShopError as e:
    print(f"Ошибка: {e}", file=sys.stderr)
    sys.exit(1)
finally:
    # 5. ВАЖНО: всегда закрываем соединение с БД, даже если была ошибка
    connection.close()


if __name__ == "__main__":
    main()
