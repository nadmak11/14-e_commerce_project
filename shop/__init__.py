import logging

# Настраиваем базовую конфигурацию логирования для всего пакета.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# "Поднимаем" классы на уровень пакета shop для удобного импорта
from .repository import StoreRepository
from .logic.orders import OrderService
