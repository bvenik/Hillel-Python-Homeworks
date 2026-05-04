import asyncio


async def producer(queue: asyncio.Queue, consumers: int) -> None:
    """
    Produces 5 tasks with a delay and sends stop signals.
    :param queue: The queue to put tasks into
    :param consumers: Number of consumers to stop
    :return: nothing
    """
    for i in range(5):
        await asyncio.sleep(1)
        await queue.put(i)
        print(f"Produced | Task: {i}")

    for n in range(consumers):
        await queue.put(None)


async def consumer(consumer_name: str, queue: asyncio.Queue) -> None:
    """
    Takes tasks from the queue and simulates work.
    :param consumer_name: Name of the consumer
    :param queue: The shared queue
    :return: nothing
    """
    while True:
        task = await queue.get()
        if task is None:
            queue.task_done()
            break

        print(f"Consumed | By: {consumer_name}. Task: {task}")
        await asyncio.sleep(2)
        queue.task_done()


async def main() -> None:
    """
    Main entry point to run producer and consumers concurrently.
    :return: nothing
    """
    queue = asyncio.Queue()
    customers = 2
    await asyncio.gather(
        producer(queue, customers),
        consumer("Consumer_1", queue),
        consumer("Consumer_2", queue)
    )

    await queue.join()


if __name__ == '__main__':
    asyncio.run(main())
