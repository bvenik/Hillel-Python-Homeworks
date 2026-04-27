"""
Завдання 4: Асинхронний таймаут
Напишіть функцію slow_task(), яка імітує виконання завдання протягом 10 секунд.
Використовуючи asyncio.wait_for(), викличте slow_task() з таймаутом 5 секунд.
Якщо завдання не встигає виконатися за цей час, виведіть повідомлення про перевищення часу очікування.
"""
import asyncio


async def slow_task(timeout_length: int | float) -> None:
    """
    Simulates slow task with timeout(timeout_length) and notifies about start/end.
    :param timeout_length: length of timeout in seconds.
    :return: nothing
    """
    print("Slow task started!")
    await asyncio.sleep(timeout_length)
    print("Slow task completed!")


async def main(timeout_length: int | float) -> None:
    """
    Initializes try/except block, if slow_task with timeout_length seconds is greater than 5 -> goes to except block. If less than 5, successfully finishes task.
    :param timeout_length: length of timeout in seconds.
    :return: nothing
    """
    print(f"Launching slow_task | Timeout length: {timeout_length}")
    try:
        await asyncio.wait_for(slow_task(timeout_length), timeout=5)
    except asyncio.TimeoutError:
        print("Timeout!")


asyncio.run(main(2))
asyncio.run(main(6))
asyncio.run(main(5))
