# setup.py
from setuptools import setup, find_packages

setup(
    name="shop_package",          # Имя пакета для pip
    version="0.1.0",              # Версия
    author="Твоё Имя",
    description="Простой пакет для имитации работы интернет-магазина",
    packages=find_packages(),     # Автоматически найти все пакеты (shop, shop.data и т.д.)
    install_requires=[            # Список зависимостей, как в requirements.txt
        "requests",
    ],
    python_requires=">=3.7",      # Требуемая версия Python
)