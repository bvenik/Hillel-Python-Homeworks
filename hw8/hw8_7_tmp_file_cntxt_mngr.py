class FileProcessor:
    """Клас для роботи з файловими операціями."""

    @staticmethod
    def write_to_file(file_path: str, data: str) -> None:
        """
        Записує рядкові дані у вказаний файл.
        :param file_path: Шлях до файлу (рядок або об'єкт шляху).
        :param data: Текст, який потрібно записати.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)

    @staticmethod
    def read_from_file(file_path: str) -> str:
        """
        Читає вміст файлу та повертає його як рядок.
        :param file_path: Шлях до файлу.
        :return: Вміст файлу.
        """
        with open(file_path, "r", encoding='utf-8') as file:
            return file.read()


def test_file_write_read(tmpdir):
    """
    Тестування коректності запису та читання за допомогою тимчасового файлу.
    :param tmpdir: Фікстура pytest для створення тимчасових директорій.
    """
    file = tmpdir.join("testfile.txt")
    FileProcessor.write_to_file(file, "Hello, World!")
    content = FileProcessor.read_from_file(file)
    assert content == "Hello, World!"
