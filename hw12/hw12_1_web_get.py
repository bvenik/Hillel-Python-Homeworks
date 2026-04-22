import requests
import threading


def download_file(url: str, filename: str) -> None:
    """
    Downloads file from webpage(url) and saves it as file(filename) in code launch directory.
    :param url: webpage url
    :param filename: output file name
    :return: nothing
    """
    thread_name = threading.current_thread().name
    print(f"Downloading, {thread_name}: {filename}")
    try:

        response = requests.get(url)

        response.raise_for_status()
        print(f"Finished, {thread_name}: {filename}")
        with open(filename, 'wb') as f:
            f.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


to_download_urls = [("https://picsum.photos/200", "file1.png"), ("https://picsum.photos/200", "file2.png"),
                    ("https://picsum.photos/200", "file3.png")]
threads = []

for url1, filename1 in to_download_urls:
    t = threading.Thread(target=download_file, args=(url1, filename1,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
