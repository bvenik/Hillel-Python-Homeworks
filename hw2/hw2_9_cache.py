def memoize(func):
    """
    Декоратор для кешування результатів функцій. Створює словник cache, який зберігає результати обчислень
    """
    cache = {}

    def wrapper(i: int) -> int:
        """
        Перевіряє, чи було число (i) вже використане, закешоване
        """
        if i not in cache:
            cache[i] = func(i)
        return cache[i]

    return wrapper


@memoize
def factorial(i: int) -> int:
    """
    Обчислення факторіала
    """
    if i == 0 or i == 1:
        return 1
    return i * factorial(i - 1)


@memoize
def fibonacci(n: int) -> int:
    """
    Обчислення чисел Фібоначчі
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(f"10!: {factorial(10)}")
print(f"30!: {factorial(30)}")
print(f"Fibonacci by 40: {fibonacci(40)}")
print(f"Fibonacci by 100: {fibonacci(100)}")
