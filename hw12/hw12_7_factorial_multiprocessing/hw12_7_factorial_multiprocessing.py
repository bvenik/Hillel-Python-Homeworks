import multiprocessing
import math


def partial_factorial(range_tuple: tuple[int, int]) -> int:
    """
    Calculates the product of numbers in a given range.
    :param range_tuple: tuple containing (start_number, end_number)
    :return: product of all integers in the range
    """
    start, end = range_tuple
    return math.prod(range(start, end + 1))


if __name__ == "__main__":
    number = 321
    cpus = multiprocessing.cpu_count()
    step = number // cpus

    ranges = [
        (i * step + 1, (i + 1) * step if i < cpus - 1 else number)
        for i in range(cpus)
    ]

    with multiprocessing.Pool(processes=cpus) as pool:
        results = pool.map(partial_factorial, ranges)
    print(math.prod(results))
