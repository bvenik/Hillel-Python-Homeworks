import math


class Fractions:
    def __init__(self, numerator, denominator) -> None:
        """
        Ініціалізація класу
        gcd - найбільший спільний дільник
        :param numerator: Чисельник дрібу
        :param denominator: Знаменник дрібу
        """
        gcd = math.gcd(numerator, denominator)
        self.numerator = numerator // gcd
        self.denominator = denominator // gcd
        if denominator == 0:
            raise ValueError("Error, denominator cannot be zero!")

    def __add__(self, other) -> Fractions:
        """
        Відповідає за додавання дробів
        :param other: Другі чисельник та знаменник
        """
        return Fractions((self.numerator * other.denominator) + (self.denominator * other.numerator),
                         self.denominator * other.denominator)

    def __sub__(self, other) -> Fractions:
        """
        Відповідає за віднімання дробів
        :param other: Другі чисельник та знаменник
        """
        return Fractions((self.numerator * other.denominator) - (self.denominator * other.numerator),
                         self.denominator * other.denominator)

    def __mul__(self, other) -> Fractions:
        """
        Відповідає за множення дробів
        :param other: Другі чисельник та знаменник
        """
        return Fractions(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other) -> Fractions:
        """
        Відповідає за ділення дробів
        :param other: Другі чисельник та знаменник
        """
        return Fractions(self.numerator * other.denominator, self.denominator * other.numerator)

    def __repr__(self) -> str:
        """
        Повертає усі обчислення та заміняє print
        """
        return f"{self.numerator}/{self.denominator}"


frac1 = Fractions(2, 3)
frac2 = Fractions(13, 7)
print(frac1 + frac2)
print(frac1 - frac2)
print(frac1 * frac2)
print(frac1 / frac2)
