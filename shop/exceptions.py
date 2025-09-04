class ShopError(Exception):
    """Базовое исключение для всех ошибок нашего магазина."""

    pass


class ProductNotFoundError(ShopError):
    """Исключение, которое выбрасывается, когда товар не найден."""

    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f"Товар с ID '{product_id}' не найден.")


class InsufficientStockError(ShopError):
    """Исключение, которое выбрасывается, когда товара недостаточно на складе."""

    def __init__(self, product_name: str, requested: int, available: int):
        self.product_name = product_name
        self.requested = requested
        self.available = available
        super().__init__(
            f"Недостаточно товара '{product_name}'. "
            f"Запрошено: {requested}, в наличии: {available}"
        )


class CurrencyConversionError(ShopError):
    """Исключение для ошибок при конвертации валюты."""

    pass
