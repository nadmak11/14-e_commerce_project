import inspect
import sys

print("--- НАЧАЛО ДИАГНОСТИКИ ---")
print(f"Версия Python: {sys.version}")
print(f"Исполняемый файл Python: {sys.executable}")
print("-" * 20)

try:
    # Пытаемся импортировать наш проблемный модуль и класс
    from shop.logic.orders import OrderService
    print("УСПЕХ: Модуль 'shop.logic.orders' и класс 'OrderService' были найдены и импортированы.")
    print("-" * 20)
    
    # Узнаем, из какого файла был загружен модуль
    orders_module = sys.modules['shop.logic.orders']
    print(f"РЕАЛЬНЫЙ ПУТЬ К ФАЙЛУ МОДУЛЯ:\n{orders_module.__file__}\n")
    print("-" * 20)
    
    # Получаем и печатаем исходный код класса, который видит Python
    print("ИСХОДНЫЙ КОД КЛАССА OrderService, КОТОРЫЙ ВИДИТ PYTHON:")
    source_code = inspect.getsource(OrderService)
    print(source_code)
    
except ImportError as e:
    print(f"КРИТИЧЕСКАЯ ОШИБКА ИМПОРТА: Не удалось найти модуль. Ошибка: {e}")
except Exception as e:
    print(f"НЕОЖИДАННАЯ ОШИБКА: {e}")

print("--- КОНЕЦ ДИАГНОСТИКИ ---")