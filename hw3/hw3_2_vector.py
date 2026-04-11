import math as m


class Vector:
    def __init__(self, x, y) -> None:
        """
        Ініціалізація класу
        :param x: x координата вектора
        :param y: y координата вектора
        """
        self.x = x
        self.y = y

    def get_length(self) -> int | float:
        """
        Отримує довжину вектора за формулою
        """
        return m.sqrt((self.x ** 2 + self.y ** 2))

    def __add__(self, other) -> Vector:
        """
        Обчислює суму векторів
        :param other: координати іншого вектора
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Vector:
        """
        Обчислює різницю векторів
        :param other: координати іншого вектора
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, k) -> Vector:
        """
        Множить ВЕКТОР на КОЕФІЦІЄНТ
        :param k: коефіцієнт(число, на яке множиться)
        """
        return Vector(self.x * k, self.y * k)

    def __truediv__(self, k) -> Vector:
        """
        Ділить ВЕКТОР на КОЕФІЦІЄНТ
        :param k: коефіцієнт(число, на яке ділиться)
        """
        if k == 0:
            raise ZeroDivisionError("Error! Division by zero is not allowed")
        else:
            return Vector(round(self.x / k, 3), round(self.y / k, 3))

    def __gt__(self, other) -> bool:
        """
        Порівнює довжини вектора, чи більше вектор(його довжина)1 за вектор(його довжина)2
        :param other: координати іншого вектора
        """
        return self.get_length() > other.get_length()

    def __lt__(self, other) -> bool:
        """
        Порівнює довжини вектора, чи менше вектор(його довжина)1 за вектор(його довжина)2
        :param other: координати іншого вектора
        """
        return self.get_length() < other.get_length()

    def __eq__(self, other) -> bool:
        """
        Порівнює довжини вектора, чи дорівнює вектор(його довжина)1 вектору(його довжині)2
        :param other: координати іншого вектора
        """
        return self.get_length() == other.get_length()

    def __repr__(self) -> str:
        """
        Повертає обчислення(__add__ __sub__ __mul__ __truediv__ __repr__) та заміняє print
        """
        return f"Vector coordinates: ({self.x}; {self.y})"


vector1 = Vector(4, 3)
vector2 = Vector(5, 6)
print(vector1.get_length())
print(vector1 + vector2)
print(vector1 - vector2)
print(vector1 * 2)
print(vector1 / 3)
print(vector1 < vector2)
print(vector1 > vector2)
print(vector1 == vector2)
print(vector1)
