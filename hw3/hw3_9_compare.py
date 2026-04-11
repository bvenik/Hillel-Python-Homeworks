class ProductWithGetSet:
    def __init__(self, name: str, price: float) -> None:
        """
        Ініціалізація класу
        """
        self.name = name
        self.set_price(price)

    def get_price(self) -> float:
        """
        Повертає ціну товару
        """
        return self._price

    def set_price(self, value: float) -> None:
        """
        Встановлює ціну товару з перевіркою
        """
        if value < 0:
            raise ValueError("Price must be greater than 0")
        self._price = value

    def __repr__(self) -> str:
        """
        Заміняє print
        """
        return f"Product(GetSet): {self.name}, {self._price}"


class ProductWithProperty:
    def __init__(self, name: str, price: float) -> None:
        """
        Ініціалізація класу
        """
        self.name = name
        self.price = price

    @property
    def price(self) -> float:
        """
        Геттер для ціни
        """
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Сеттер для ціни з перевіркою
        """
        if value < 0:
            raise ValueError("Price must be greater than 0")
        self._price = value

    def __repr__(self) -> str:
        """
        Заміняє print
        """
        return f"Product(Property): {self.name}, {self._price}"


class PriceDescriptor:
    def __init__(self, attribute_name: str) -> None:
        """
        Ініціалізація дескриптора
        """
        self.attribute_name = f"_{attribute_name}"

    def __get__(self, instance, owner) -> float:
        """
        Метод отримання значення через дескриптор
        """
        return getattr(instance, self.attribute_name)

    def __set__(self, instance, value: float) -> None:
        """
        Метод встановлення значення через дескриптор
        """
        if value < 0:
            raise ValueError("Price must be greater than 0")
        setattr(instance, self.attribute_name, value)


class ProductWithDescriptor:
    price = PriceDescriptor("price")

    def __init__(self, name: str, price: float) -> None:
        """
        Ініціалізація класу
        """
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        """
        Заміняє print
        """
        return f"Product(Descriptor): {self.name}, {self.price}"


products = [
    ProductWithGetSet("Apple", 25.5),
    ProductWithProperty("Banana", 40.0),
    ProductWithDescriptor("Orange", 60.0)
]

for p in products:
    print(p)

for p in products:
    try:
        print(f"Trying place -10 for {type(p).__name__}")
        if isinstance(p, ProductWithGetSet):
            p.set_price(-10)
        else:
            p.price = -10
    except ValueError as e:
        print(f"Error: {e}")
