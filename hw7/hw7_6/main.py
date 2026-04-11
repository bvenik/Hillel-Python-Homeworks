import json
import csv
import xml.etree.ElementTree as ET


class FileConverter:
    """Базовий інтерфейс для всіх конвертерів файлів."""
    total_conversions = 0

    def __init__(self, input_file: str, output_file: str):
        """
        Ініціалізує конвертер шляхами до файлів.

        :param input_file: Шлях до вхідного файлу.
        :param output_file: Шлях до вихідного файлу.
        """
        self.input_file = input_file
        self.output_file = output_file

    def convert(self) -> None:
        """Метод, який мають реалізувати всі нащадки."""
        pass

    def _counter(self):
        """Внутрішній метод для логування ітерацій (твій flag)."""
        FileConverter.total_conversions += 1
        print(f"\nIteration {FileConverter.total_conversions}\n{self.input_file}' -> '{self.output_file}")


class CSVToJSONConverter(FileConverter):
    """Конвертер з формату CSV у JSON. Наслілдує клас FileConverter"""

    def convert(self) -> None:
        """Зчитує CSV та зберігає дані у форматі JSON."""
        self._counter()
        data = []

        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            print(f"Error! '{self.input_file}' not found!")

        if data:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Success: {self.output_file} created.")
        else:
            print(f"Failure: '{self.output_file}' wasn't created")


CSVToJSONConverter('test1_input.csv', 'test1_output.json').convert()
CSVToJSONConverter('test_not_exist.csv', 'test1.json').convert()


class JSONToCSVConverter(FileConverter):
    """Конвертер з формату JSON у CSV. Наслідує клас FileConverter"""

    def convert(self) -> None:
        """Зчитує JSON та зберігає дані у форматі CSV."""
        self._counter()
        data = []

        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error! Cannot read JSON from '{self.input_file}': {e}")

        if data and isinstance(data, list) and len(data) > 0:
            headers = data[0].keys()

            with open(self.output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data[1:])
            print(f"Success: {self.output_file} created from JSON.")
        else:
            print(f"Failure: '{self.output_file}' wasn't created")


JSONToCSVConverter('test2_input.json', 'test2_output.csv').convert()
JSONToCSVConverter('test2_not_exist.json', 'test2.json').convert()


class XMLToJSONConverter(FileConverter):
    """Конвертер з формату XML у JSON. Наслідує клас FileConverter."""

    def convert(self) -> None:
        """Зчитує XML та зберігає дані у форматі JSON."""
        self._counter()
        data = []
        try:
            root = ET.parse(self.input_file).getroot()
            for item in root:
                items = {}
                for child in item:
                    items[child.tag] = child.text
                data.append(items)
        except (FileNotFoundError, ET.ParseError) as e:
            print(f"Error! Cannot read XML from '{self.input_file}': {e}")

        if data:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Success: {self.output_file} created.")
        else:
            print(f"Failure: '{self.output_file}' wasn't created")


XMLToJSONConverter('test3_input.xml', 'test3_output.json').convert()
XMLToJSONConverter('test3_not_exist..xml', 'test3_output.json').convert()
