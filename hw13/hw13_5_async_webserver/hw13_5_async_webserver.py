import asyncio
from aiohttp import web


async def default_path(request: web.Request) -> web.Response:
    """
    Simulates root path.
    :param request: incoming HTTP request
    :return: response with Hello World text
    """
    return web.Response(text="Hello, World!")


async def slow_path(request: web.Request) -> web.Response:
    """
    Simulates a long task with a 5-second delay.
    :param request: incoming HTTP request
    :return: response after delay
    """
    await asyncio.sleep(5)
    return web.Response(text="Operation completed!")


async def main() -> None:
    """
    Sets up and starts the asynchronous web server on localhost:8000.
    :return: nothing
    """
    app = web.Application()
    app.add_routes(
        [
            web.get("/", default_path),
            web.get("/slow", slow_path),
        ]
    )
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="localhost", port=8000)
    print("Starting server on a http://localhost:8000 ")
    await site.start()
    while True:
        await asyncio.sleep(10000)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped")
