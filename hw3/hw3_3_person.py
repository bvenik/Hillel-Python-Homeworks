class Person:

    def __init__(self, name: str, age: int) -> None:
        """
        Ініціалізація класу
        :param name: ім'я
        :param age: вік
        """
        self.name = name
        self.age = age

    def __lt__(self, other) -> bool:
        """
        Порівнює вік(age) двох різних об'єктів за оператором <
        :param other: інший об'єкт класу Person для порівняння
        """
        return self.age < other.age

    def __gt__(self, other) -> bool:
        """
        Порівнює вік(age) двох різних об'єктів за оператором >
        :param other: інший об'єкт класу Person для порівняння
        """
        return self.age > other.age

    def __eq__(self, other) -> bool:
        """
        Порівнює вік(age) двох різних об'єктів за оператором ==
        :param other: інший об'єкт класу Person для порівняння
        """
        return self.age == other.age

    def __repr__(self) -> str:
        """
        Обробляє зовнішній вигляд даних name та age при друкуванні
        """
        return f"{self.name} - {self.age}"


p1 = Person("Benjamin", 32)
p2 = Person("Franklin", 47)
p3 = Person("Kevin", 12)
people = [p1, p2, p3]
print(people)
print(p1 < p2)
print(p1 > p2)
print(p3 == p2)
sorted_people = sorted(people)
print(sorted_people)
