"""
Задача 3: підрахунок суми чисел у великому масиві
Створіть програму, яка ділить великий масив чисел на кілька частин
і рахує суму кожної частини паралельно в різних процесах. Використовуйте модуль multiprocessing.
"""

import multiprocessing


def array_sum(array: list) -> int | float:
    """
    Summing every number in an array(array) and returns one number.
    :param array: array to be summed.
    :return: nothing
    """
    return sum(array)


if __name__ == '__main__':
    num_array = list(range(1000000))
    cpu_count = multiprocessing.cpu_count()
    chunk_size = len(num_array) // cpu_count
    chunks = [num_array[i: i + chunk_size] for i in range(0, len(num_array), chunk_size)]
    with multiprocessing.Pool(processes=cpu_count) as pool:
        results = pool.map(array_sum, chunks)
    total_sum = sum(results)
    print(f"Chunks: {results}")
    print(f"Sum result: {total_sum}")
