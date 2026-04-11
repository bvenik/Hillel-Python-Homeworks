class MyClass:
    def __init__(self, mylist: list) -> None:
        """
        Ініціалізація класу
        :param mylist: список цілих чисел
        """
        self.mylist = mylist

    def __len__(self) -> int:
        """
        Повертає кількість елементів у списку
        """
        count = 0
        for _ in self.mylist:
            count += 1
        return count

    def sum(self) -> int:
        """
        Обчислює суму всіх елементів списку
        """
        total = 0
        for i in self.mylist:
            total += i
        return total

    def min(self) -> int | str:
        """
        Знаходить мінімальне значення у списку
        """
        if not self.mylist:
            return "Can't find minimum! List is empty!"

        minimum = self.mylist[0]
        for i in self.mylist:
            if i < minimum:
                minimum = i
        return minimum

    def __repr__(self) -> str:
        """
        Повертає рядкове представлення списку
        """
        return str(self.mylist)


mc = MyClass([121, 4, 3, 23, 2, 5, 0, -123, 4, 32, 23])
mc2 = MyClass([])
print(mc)
print(len(mc))
print(mc.sum())
print(mc.min())

print(mc2)
print(len(mc2))
print(mc2.sum())
print(mc2.min())
