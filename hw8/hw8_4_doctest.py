def is_even(n: int) -> bool:
    """
    Перевіряє, чи є число парним.

    >>> is_even(2)
    True
    >>> is_even(3)
    False
    """
    return n % 2 == 0


def factorial(n: int) -> int:
    """
    Повертає факторіал числа n.

    >>> factorial(5)
    120
    >>> factorial(0)
    1
    """
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res