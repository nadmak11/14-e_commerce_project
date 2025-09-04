import sqlite3
import logging
from typing import Optional
from .models import Product

log = logging.getLogger(__name__)


class StoreRepository:
    def __init__(self, connection: sqlite3.Connection):
        self._con = connection
        log.info("Хранилище инициализировано с подключением к базе данных.")

    def get_product_details(self, product_id: str) -> Optional[Product]:
        """
        Возвращает детали товара из БД в виде объекта Product.
        """
        cursor = self._con.cursor()
        # Используем '?' для безопасной подстановки параметров, это защищает от SQL-инъекций
        cursor.execute(
            "SELECT id, name, price FROM products WHERE id = ?", (product_id,)
        )
        row = cursor.fetchone()

        if row:
            # row - это кортеж (tuple), например ('p1', 'Ноутбук', 80000)
            return Product(id=row[0], name=row[1], price=row[2])
        return None

    def get_stock(self, product_id: str) -> int:
        """Возвращает количество товара на складе из БД."""
        cursor = self._con.cursor()
        cursor.execute(
            "SELECT quantity FROM inventory WHERE product_id = ?", (product_id,)
        )
        row = cursor.fetchone()
        return row[0] if row else 0

    def update_stock(self, product_id: str, new_quantity: int) -> None:
        """Обновляет количество товара на складе в БД."""
        log.info(f"Обновление склада в БД: {product_id}, новое кол-во: {new_quantity}")
        cursor = self._con.cursor()
        cursor.execute(
            "UPDATE inventory SET quantity = ? WHERE product_id = ?",
            (new_quantity, product_id),
        )
        # commit() нужен для сохранения любых изменений (INSERT, UPDATE, DELETE)
        self._con.commit()
