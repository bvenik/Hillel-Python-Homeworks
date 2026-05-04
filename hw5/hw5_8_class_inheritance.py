def analyze_inheritance(cls: type) -> None:
    """
    Аналізує спадкування класу та виводить методи, отримані від базових класів.
    :param cls: клас, який аналізується
    :return: None
    """
    print(f"Клас {cls.__name__} наслідує:")
    for base in cls.__mro__:
        if base is cls or base is object:
            continue

        for method_name in vars(base):
            attr_value = getattr(base, method_name)

            if callable(attr_value) and not method_name.startswith("__"):
                print(f"- {method_name} з {base.__name__}")


class GrandParent:
    """
    Базовий клас верхнього рівня.
    """

    def grandparent_method(self) -> None:
        """
        Метод діда.
        :return: None
        """
        pass


class Parent(GrandParent):
    """
    Батьківський клас, що наслідує GrandParent.
    """

    def parent_method(self) -> None:
        """
        Метод батька.
        :return: None
        """
        pass


class Child(Parent):
    """
    Дочірній клас, що наслідує Parent.
    """

    def child_method(self) -> None:
        """
        Метод дитини.
        :return: None
        """
        pass


analyze_inheritance(Child)