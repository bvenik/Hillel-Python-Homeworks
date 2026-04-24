import concurrent.futures
from PIL import Image
import os


def image_processing(filepath: str) -> None:
    """
    Mirrors(pixels from left side swap with right side pixels) file(filepath) and saves as [input file name]_mirrored[input file extension].
    :param filepath: path or name of file to mirror
    :return: nothing
    """
    try:
        with Image.open(filepath) as img:
            mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            file_name, file_ext = os.path.splitext(filepath)
            new_filename = f"{file_name}_mirrored{file_ext}"
            mirrored_img.save(new_filename)
    except Exception as e:
        print(f"{e}")

#easiest way to get these files, run hw12_1_web_get.py
files_to_mirror = ["file1.png", "file2.png", "file3.png"]

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(image_processing, files_to_mirror)
