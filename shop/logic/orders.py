import logging
from ..repository import StoreRepository
from ..utils.currency import convert_rub_to
from ..exceptions import (
    ProductNotFoundError,
    InsufficientStockError,
    CurrencyConversionError,
)

log = logging.getLogger(__name__)


class OrderService:
    def __init__(self, repository: StoreRepository):
        self._repository = repository

    def create_order(
        self, product_id: str, quantity: int, currency: str = "RUB"
    ) -> str:
        log.info(
            f"Попытка создать заказ: товар={product_id}, кол-во={quantity}, валюта={currency}"
        )

        product = self._repository.get_product_details(product_id)
        if not product:
            # Вместо возврата строки, выбрасываем исключение
            raise ProductNotFoundError(product_id=product_id)

        stock = self._repository.get_stock(product_id)
        if stock < quantity:
            # Выбрасываем другое, более специфичное исключение
            raise InsufficientStockError(
                product_name=product.name, requested=quantity, available=stock
            )

        # Используем атрибуты объекта: product.price вместо product['price']
        total_price_rub = product.price * quantity

        if currency.upper() != "RUB":
            converted_price = convert_rub_to(currency, total_price_rub)
            if converted_price is None:
                log.error("Не удалось сконвертировать цену. Заказ отменен.")
                raise CurrencyConversionError(
                    "Сервис валют не ответил или не нашёл валюту."
                )
            final_price = converted_price
        else:
            final_price = total_price_rub

        new_stock = stock - quantity
        self._repository.update_stock(product_id, new_stock)

        log.info(f"Заказ для товара '{product.name}' успешно создан.")
        return (
            f"Заказ успешно создан! "
            f"Товар: {product.name}, "
            f"Количество: {quantity} шт., "
            f"Сумма: {final_price} {currency.upper()}. "
            f"Остаток на складе: {new_stock} шт."
        )
