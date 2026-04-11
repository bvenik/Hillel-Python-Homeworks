import pytest


def divide(a: int | float, b: int | float) -> float:
    """
    Виконує ділення двох чисел.
    :param a: Чисельник (int або float).
    :param b: Знаменник (int або float).
    :return: Результат ділення як float.
    """
    return a / b


@pytest.mark.parametrize("a, b, exp_val", [
    (1, 2, 0.5),
    (4, 4, 1),
    (3, 5, 3 / 5),
    (0, 2, 0),
    (-20, 5, -4),
    (-4, -0.5, 8)
])
def test_divide(a: int | float, b: int | float, exp_val: int | float) -> None:
    """
    Тестує функцію divide з різними комбінаціями чисел.
    Перевіряє позитивні, негативні числа та ділення нуля.
    """
    assert divide(a, b) == exp_val


def test_divide_zero() -> None:
    """
    Перевіряє, чи виникає виключення ZeroDivisionError при діленні на нуль.
    """
    with pytest.raises(ZeroDivisionError):
        divide(3, 0)
