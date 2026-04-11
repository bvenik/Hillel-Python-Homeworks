class BinaryNumber:

    def __init__(self, binary: int) -> None:
        """
        Ініціалізація класу
        :param binary: число в десятковій системі
        """
        self.binary = binary

    def __and__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        """
        Виконує побітову операцію І (AND)
        :param other: інший об'єкт класу BinaryNumber
        """
        return BinaryNumber(self.binary & other.binary)

    def __or__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        """
        Виконує побітову операцію АБО (OR)
        :param other: інший об'єкт класу BinaryNumber
        """
        return BinaryNumber(self.binary | other.binary)

    def __xor__(self, other: 'BinaryNumber') -> 'BinaryNumber':
        """
        Виконує побітову операцію виключне АБО (XOR)
        :param other: інший об'єкт класу BinaryNumber
        """
        return BinaryNumber(self.binary ^ other.binary)

    def __invert__(self) -> 'BinaryNumber':
        """
        Виконує побітову операцію НЕ (NOT)
        """
        return BinaryNumber(~self.binary)

    def __repr__(self) -> str:
        """
        Обробляє зовнішній вигляд даних binary при друкуванні
        """
        return f"{bin(self.binary)}, {self.binary}"


num1 = BinaryNumber(14)
num2 = BinaryNumber(10)
print(num1 & num2)
print(num1 | num2)
print(num1 ^ num2)
print(~num1)
print(~num2)
