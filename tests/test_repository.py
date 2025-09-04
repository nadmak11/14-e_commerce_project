import sqlite3
import pytest
from shop.repository import StoreRepository


@pytest.fixture
def db_connection():
    """
    Фикстура, которая создает чистую базу данных в памяти для каждого теста.
    """
    # ':memory:' - специальное имя для создания БД в ОЗУ
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    # Создаем таблицы
    cur.execute("CREATE TABLE products (id TEXT PRIMARY KEY, name TEXT, price INTEGER)")
    cur.execute(
        "CREATE TABLE inventory (product_id TEXT PRIMARY KEY, quantity INTEGER)"
    )

    # Вставляем тестовые данные
    cur.execute("INSERT INTO products VALUES ('p1', 'Тестовый Ноутбук', 100)")
    cur.execute("INSERT INTO inventory VALUES ('p1', 10)")

    con.commit()

    # yield возвращает созданное соединение в тест
    yield con

    # Код после yield выполнится после завершения теста (очистка)
    con.close()


def test_get_product_details(db_connection):
    """Проверяем, что репозиторий корректно получает данные из БД."""
    repo = StoreRepository(connection=db_connection)
    product = repo.get_product_details("p1")
    assert product is not None
    assert product.name == "Тестовый Ноутбук"
    assert product.price == 100


def test_get_stock(db_connection):
    """Проверяем, что репозиторий корректно получает остаток из БД."""
    repo = StoreRepository(connection=db_connection)
    stock = repo.get_stock("p1")
    assert stock == 10


def test_update_stock(db_connection):
    """Проверяем, что репозиторий корректно обновляет остаток в БД."""
    repo = StoreRepository(connection=db_connection)

    # Обновляем данные
    repo.update_stock("p1", 5)

    # Проверяем, что данные действительно изменились
    cursor = db_connection.cursor()
    cursor.execute("SELECT quantity FROM inventory WHERE product_id = 'p1'")
    new_stock = cursor.fetchone()[0]
    assert new_stock == 5
