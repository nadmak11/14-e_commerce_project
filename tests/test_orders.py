import pytest
from shop.logic.orders import OrderService
from shop.models import Product
from shop.exceptions import InsufficientStockError, ProductNotFoundError


def test_create_order_success(mocker):
    mock_repo = mocker.MagicMock()

    # Теперь мок должен возвращать объект Product, а не словарь
    mock_repo.get_product_details.return_value = Product(
        id="p1", name="Ноутбук", price=80000
    )
    mock_repo.get_stock.return_value = 10

    order_service = OrderService(repository=mock_repo)
    result = order_service.create_order(product_id="p1", quantity=2)

    assert "Заказ успешно создан" in result
    assert "Остаток на складе: 8 шт." in result
    mock_repo.update_stock.assert_called_once_with("p1", 8)


def test_create_order_insufficient_stock(mocker):
    mock_repo = mocker.MagicMock()
    mock_repo.get_product_details.return_value = Product(
        id="p1", name="Ноутбук", price=80000
    )
    mock_repo.get_stock.return_value = 1

    order_service = OrderService(repository=mock_repo)

    # Используем pytest.raises для проверки, что код выбрасывает нужное исключение
    with pytest.raises(InsufficientStockError) as exc_info:
        order_service.create_order(product_id="p1", quantity=2)

    # Можно даже проверить содержимое исключения
    assert "Запрошено: 2, в наличии: 1" in str(exc_info.value)

    mock_repo.update_stock.assert_not_called()


def test_create_order_product_not_found(mocker):
    """Новый тест для проверки случая, когда товар не найден."""
    mock_repo = mocker.MagicMock()
    # Мок возвращает None, как будто товара нет в базе
    mock_repo.get_product_details.return_value = None

    order_service = OrderService(repository=mock_repo)

    with pytest.raises(ProductNotFoundError):
        order_service.create_order(product_id="p_non_existent", quantity=1)
