import math as m


class Vector:
    def __init__(self, *dimensions) -> None:
        """
        Ініціалізація класу
        """
        self.dimensions = dimensions

    def __add__(self, other) -> Vector:
        """
        Обчислює суму векторів
        :param other: координати іншого вектора
        """
        if len(self.dimensions) != len(other.dimensions):
            raise "Impossible! Quantity of dimension mismatch!"
        new_coords = []
        for a, b in zip(self.dimensions, other.dimensions):
            new_coords.append(a + b)
        return Vector(*new_coords)

    def __sub__(self, other) -> Vector:
        if len(self.dimensions) != len(other.dimensions):
            raise "Impossible! Quantity of dimension mismatch!"
        new_coords = []
        for a, b in zip(self.dimensions, other.dimensions):
            new_coords.append(a - b)
        return Vector(*new_coords)

    def __mul__(self, other) -> int | float:
        if len(self.dimensions) != len(other.dimensions):
            raise "Impossible! Quantity of dimension mismatch!"
        value = 0
        for a, b in zip(self.dimensions, other.dimensions):
            value += a * b
        return value

    def get_length(self) -> int | float:
        """
        Отримує довжину вектора за формулою
        """
        sum_of_squares = 0
        for x in self.dimensions:
            sum_of_squares += x ** 2
        return round(m.sqrt(sum_of_squares), 3)

    def __gt__(self, other) -> bool:
        """
        Порівнює довжини вектора, чи більше вектор(його довжина)1 за вектор(його довжина)2
        :param other: координати іншого вектора
        """
        if len(self.dimensions) != len(other.dimensions):
            raise "Impossible! Quantity of dimension mismatch!"
        return self.get_length() > other.get_length()

    def __lt__(self, other) -> bool:
        """
        Порівнює довжини вектора, чи менше вектор(його довжина)1 за вектор(його довжина)2
        :param other: координати іншого вектора
        """
        if len(self.dimensions) != len(other.dimensions):
            raise "Impossible! Quantity of dimension mismatch!"
        return self.get_length() < other.get_length()

    def __eq__(self, other) -> bool:
        """
        Порівнює довжини вектора, чи дорівнює вектор(його довжина)1 вектору(його довжині)2
        :param other: координати іншого вектора
        """
        if len(self.dimensions) != len(other.dimensions):
            raise "Impossible! Quantity of dimension mismatch!"
        return self.get_length() == other.get_length()

    def __repr__(self) -> str:
        """
        Повертає обчислення(__add__ __sub__ __mul__ __truediv__ __repr__) та заміняє print
        """
        return f"Vector coordinates: {self.dimensions}"


vec1 = Vector(3, 2, 5, -23214)
vec2 = Vector(4, 7, 123, 9)
print(vec1)
print(vec2)
print(vec1 + vec2)
print(vec1 - vec2)
print(vec1 * vec2)
print(vec1.get_length())
print(vec2.get_length())
print(vec1 > vec2)
print(vec1 < vec2)
print(vec1 == vec2)
