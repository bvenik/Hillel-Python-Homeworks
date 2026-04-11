import pytest


class AgeVerifier:
    """Клас для перевірки віку користувачів."""

    @staticmethod
    def is_adult(age: int) -> bool:
        """Повертає True, якщо вік більше або дорівнює 18.
        :param age: Вік користувача.
        :return: Статус повноліття."""
        return age >= 18


def test_is_adult_normal():
    """Перевірка коректної роботи для стандартних значень."""
    assert AgeVerifier.is_adult(20) == True
    assert AgeVerifier.is_adult(16) == False


@pytest.mark.skip(reason="Некоректне значення: вік менший за 0")
def test_negative_age():
    """Цей тест буде пропущено завжди через маркер skip."""
    assert AgeVerifier.is_adult(-5) == False


@pytest.mark.skipif(121 > 120, reason="Неправильне значення: винятково великий можливий вік")
def test_is_adult_extreme():
    """Пропускаємо, якщо вік більше за 120."""
    assert AgeVerifier.is_adult(121) == True
