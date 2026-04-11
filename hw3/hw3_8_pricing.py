class Price:
    def __init__(self, price: int | float) -> None:
        """
        Ініціалізація класу, перевірка на валідність price
        :param price: початкова ціна
        """
        if price >= 0:
            self.price = round(price, 2)
        else:
            raise "Price must be equal or greater than 0"

    def __add__(self, other) -> Price:
        """
        Обчислює суму
        :param other: інше число(ціна(price))
        """
        return Price(self.price + other.price)

    def __sub__(self, other) -> Price:
        """
        Обчислює різницю у випадку, якщо вона буде більше або дорівнюватиме 0
        :param other: інше число(ціна(price))
        """
        if other.price > self.price:
            raise "Resulted price must be equal or greater than the 0"
        return Price(self.price - other.price)

    def __gt__(self, other) -> bool:
        """
        Порівнює першу ціну(self.price) і другу ціну(other.price) за оператором >
        :param other: інше число(ціна(price))
        """
        return self.price > other.price

    def __lt__(self, other) -> bool:
        """
        Порівнює першу ціну(self.price) і другу ціну(other.price) за оператором <
        :param other: інше число(ціна(price))
        """
        return self.price < other.price

    def __eq__(self, other) -> bool:
        """
        Порівнює першу ціну(self.price) і другу ціну(other.price) за оператором ==
        :param other: інше число(ціна(price))
        """
        return self.price == other.price

    def __repr__(self) -> str:
        """
        Репрезентує, повертає відформатований рядок з даними self.price
        """
        return f"Price: {self.price}"


pr1 = Price(1300)
pr2 = Price(200)
print(pr1)
print(pr2)
print(pr1 + pr2)
print(pr1 - pr2)
print(pr1 == pr2)
print(pr1 > pr2)
print(pr1 < pr2)
