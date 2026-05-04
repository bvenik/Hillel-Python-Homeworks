from typing import Generator
import csv
from pathlib import Path
from PIL import Image


def image_info(folder: str) -> Generator:
    """
    1. Шукає теку(folder) в кореневій теці (тека, там де цей виконавчий файл) та обробляє кожен файл в ній
    2. (if: else:) Умова - розширення поточного файлу(використовується формат lowercase) рівний одному з форматів зображень у списку image_extensions
    2.1. True: йде до пункту 3
    2.2. False: пропускає цей файл та іде до пункту 1
    3. (try: except:)
    3.1. try: Через менеджера контексту добуває та повертає в зображенні: Ім'я(Name), Ширина(Width), Висота(Height), Формат(Format)
    3.2. except: Обробляє та вказує на Exception
    :param folder: назва теки, яка лежить в тій же теці, де й файл виконавець
    :return: генератор, що по черзі (yield) повертає словники з метаданими кожного знайденого зображення
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.raw']
    for file in Path(folder).glob('*'):
        if file.suffix.lower() in image_extensions:
            try:
                with Image.open(file) as img:
                    w, h = img.size
                    yield {
                        "Name": file.name,
                        "Width": w,
                        "Height": h,
                        "Format": img.format,
                    }
            except Exception as e:
                print(f"Помилка у файлі {file.name}: {e}")
        else:
            print(f"Пропущено: {file.name}")


metadata = ["Name", "Width", "Height", "Format"]
output_file = "hw6_3_image_stats.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=metadata, delimiter=";")
    writer.writeheader()

    for info in image_info('hw6_3_images'):
        writer.writerow(info)
        print(f"Оброблено: {info['Name']}")
