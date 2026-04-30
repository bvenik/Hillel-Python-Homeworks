import asyncio
import aiohttp


async def download_image(session: aiohttp.ClientSession, image_url: str, name: str) -> None:
    """
    Downloads an image from a URL and saves it to a binary file.
    :param session: shared aiohttp ClientSession
    :param image_url: direct URL of the image
    :param name: filename to save the image
    :return: nothing
    """
    try:
        async with session.get(image_url) as resp:
            resp.raise_for_status()
            data = await resp.read()
            with open(name, "wb") as f:
                f.write(data)
            print(f"{name} successfully saved")
    except Exception as e:
        print(f"{name}: {e}")


async def main() -> None:
    """
    Coordinates the concurrent download of multiple images.
    :return: nothing
    """
    urls_to_download = [
        "https://picsum.photos/600/600",
        "https://picsum.photos/600/600",
        "https://picsum.photos/600/600",
        "https://pics.error/link",
    ]

    tasks = []
    async with aiohttp.ClientSession() as session:
        for i, url in enumerate(urls_to_download):
            filename = f"file{i + 1}.png"
            tasks.append(download_image(session, url, filename))

        await asyncio.gather(*tasks)


asyncio.run(main())
