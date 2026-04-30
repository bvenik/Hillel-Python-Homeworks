import asyncio
import multiprocessing
import time
import requests
import aiohttp
import concurrent.futures as futures


def fetch_sync(url: str) -> int:
    """
    Performs a synchronous HTTP GET request.
    :param url: target URL
    :return: status code
    """
    with requests.get(url) as response:
        return response.status_code


def run_sync(url: str, count: int) -> None:
    """
    Executes requests sequentially.
    :param url: target URL
    :param count: number of requests
    :return: nothing
    """
    for _ in range(count):
        fetch_sync(url)


def run_threads(url: str, count: int) -> None:
    """
    Executes requests using thread pool.
    :param url: target URL
    :param count: number of requests
    :return: nothing
    """
    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(fetch_sync, [url] * count))


def run_process(url: str, count: int) -> None:
    """
    Executes requests using process pool.
    :param url: target URL
    :param count: number of requests
    :return: nothing
    """
    with multiprocessing.Pool(processes=5) as pool:
        pool.map(fetch_sync, [url] * count)


async def fetch_async(session: aiohttp.ClientSession, url: str) -> int:
    """
    Performs an asynchronous HTTP GET request.
    :param session: shared aiohttp session
    :param url: target URL
    :return: status code
    """
    async with session.get(url) as response:
        return response.status


async def run_async(url: str, count: int) -> None:
    """
    Executes requests using asyncio.
    :param url: target URL
    :param count: number of requests
    :return: nothing
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(count):
            tasks.append(asyncio.create_task(fetch_async(session, url)))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    count = 20
    url = 'https://www.google.com'

    print(f"Starting benchmark for {count} requests...\n")

    start = time.perf_counter()
    run_sync(url, count)
    print(f"Sync: {str(time.perf_counter() - start)[:4]}s")

    start = time.perf_counter()
    run_threads(url, count)
    print(f"Threads: {str(time.perf_counter() - start)[:4]}s")

    start = time.perf_counter()
    run_process(url, count)
    print(f"Processes: {str(time.perf_counter() - start)[:4]}s")

    start = time.perf_counter()
    asyncio.run(run_async(url, count))
    print(f"Async: {str(time.perf_counter() - start)[:4]}s")
