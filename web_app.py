import os
import sqlite3
import sys
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv  # Импортируем новую библиотеку

from shop import StoreRepository, OrderService
from shop.exceptions import ShopError

# Загружаем переменные из .env файла в окружение.
# Это нужно делать до первого обращения к os.getenv()
load_dotenv()

# --- Модели данных для API (используем Pydantic) ---
# Pydantic очень похож на dataclasses, но создан специально для валидации данных в API.


class OrderRequest(BaseModel):
    """Модель запроса на создание заказа."""

    product_id: str
    quantity: int
    currency: str = "RUB"


class OrderResponse(BaseModel):
    """Модель успешного ответа после создания заказа."""

    message: str


# --- Создание приложения FastAPI ---
app = FastAPI(
    title="E-commerce Shop API",
    description="API для управления заказами в нашем интернет-магазине.",
    version="1.0.0",
)

# --- Управление зависимостями (Dependency Injection) ---


def get_db_path() -> Path:
    """
    Получает путь к БД из переменной окружения.
    Если переменная не задана, используется значение по умолчанию.
    """
    db_path_str = os.getenv("DATABASE_PATH", "data/shop.db")
    return Path(db_path_str)


def get_db_connection(db_path: Path = Depends(get_db_path)):
    """
    Функция-зависимость: создает и отдает соединение с БД для одного запроса.
    """
    if not db_path.parent.exists():
        # Создаем директорию для БД, если ее нет (полезно для первого запуска)
        db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    try:
        yield connection
    finally:
        connection.close()


def get_order_service(
    conn: sqlite3.Connection = Depends(get_db_connection),
) -> OrderService:
    """
    Функция-зависимость: собирает наш сервис.
    FastAPI автоматически вызовет `get_db_connection` и передаст результат в `conn`.
    """
    repository = StoreRepository(connection=conn)
    return OrderService(repository=repository)


# --- API эндпоинты (маршруты) ---


@app.post("/orders/", response_model=OrderResponse, tags=["Orders"])
def create_order_endpoint(
    order_data: OrderRequest, order_service: OrderService = Depends(get_order_service)
):
    """
    Создает новый заказ.

    - **product_id**: Идентификатор товара (например, 'p1').
    - **quantity**: Количество товара.
    - **currency**: Валюта (по умолчанию 'RUB').
    """
    try:
        result_message = order_service.create_order(
            product_id=order_data.product_id,
            quantity=order_data.quantity,
            currency=order_data.currency,
        )
        return OrderResponse(message=result_message)
    except ShopError as e:
        # Превращаем наши кастомные исключения в красивые HTTP-ошибки
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/", tags=["Info"])
def read_root():
    """Корневой эндпоинт для проверки, что сервис работает."""
    return {"message": "Добро пожаловать в API нашего магазина!"}
