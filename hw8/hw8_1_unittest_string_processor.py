import unittest


class StringProcessor:
    """
    Клас для обробки та маніпуляції рядками.
    """

    def reverse_string(self, s: str) -> str:
        """
        :param s: вхідний рядок
        :return: перевернута версія вхідного рядка
        """
        return s[::-1]

    def capitalize_string(self, s: str) -> str:
        """
        :param s: вхідний рядок
        :return: вхідний рядок з першим символом у верхньому регістрі
        """
        return s.capitalize()

    def count_vowels(self, s: str) -> int:

        """
        :param s: вхідний рядок
        :return: кількість голосних літер у вхідному рядку
        """
        vowels: int = 0
        for char in s:
            if char in 'aeiouAEIOU':
                vowels += 1
        return vowels


class TestStringProcessor(unittest.TestCase):
    """
    Набір модульних тестів для класу StringProcessor.
    """

    def setUp(self) -> None:
        """
        Налаштування екземпляра StringProcessor перед кожним тестом.
        """
        self.processor: StringProcessor = StringProcessor()

    def test_reverse_string(self) -> None:
        """
        Тестування методу перевертання рядка.
        """
        self.assertEqual(self.processor.reverse_string('reverse'), 'esrever')
        self.assertEqual(self.processor.reverse_string(' '), ' ')
        self.assertEqual(self.processor.reverse_string('ABc'), 'cBA')
        self.assertEqual(self.processor.reverse_string('23$hh_O'), 'O_hh$32')

    @unittest.skip("Пропуск тесту порожнього рядка")
    def test_reverse_string_empty(self) -> None:
        """
        Тестування перевертання порожнього рядка.
        """
        self.assertEqual(self.processor.reverse_string(''), '')

    def test_capitalize_string(self) -> None:
        """
        Тестування методу капіталізації першої літери.
        """
        self.assertEqual(self.processor.capitalize_string('pear'), 'Pear')
        self.assertEqual(self.processor.capitalize_string('Pineapple'), 'Pineapple')
        self.assertEqual(self.processor.capitalize_string(''), '')
        self.assertEqual(self.processor.capitalize_string(' '), ' ')
        self.assertEqual(self.processor.capitalize_string('233'), '233')

    def test_count_vowels(self) -> None:
        """
        Тестування методу підрахунку голосних.
        """
        self.assertEqual(self.processor.count_vowels('jackfruit'), 3)
        self.assertEqual(self.processor.count_vowels('123!@#'), 0)
        self.assertEqual(self.processor.count_vowels(''), 0)
        self.assertEqual(self.processor.count_vowels('GG'), 0)
        self.assertEqual(self.processor.count_vowels('aAaAaAa'), 7)


if __name__ == '__main__':
    unittest.main()
