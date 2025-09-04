from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """
    Класс данных, представляющий товар.
    frozen=True делает объекты этого класса неизменяемыми (immutable),
    что предотвращает случайное изменение цены или имени после создания.
    """

    id: str
    name: str
    price: int
