import pytest
from unittest.mock import MagicMock


class BankAccount:
    """Клас для керування банківським рахунком."""

    def __init__(self, amount: float) -> None:
        """
        Ініціалізація рахунку.
        :param amount: Початкова сума на рахунку.
        """
        self.amount = amount

    def deposit(self, amount: float) -> None:
        """
        Додає кошти на рахунок.
        :param amount: Сума для поповнення.
        """
        self.amount += amount

    def withdraw(self, amount: float) -> None:
        """
        Знімає кошти, якщо баланс дозволяє.
        :param amount: Сума для зняття.
        """
        if amount <= self.amount:
            self.amount -= amount

    def get_balance(self) -> float:
        """
        Повертає поточний баланс.
        :return: Поточний залишок на рахунку.
        """
        return self.amount


@pytest.fixture
def bank_account() -> BankAccount:
    """
    Фікстура для створення об'єкта BankAccount.
    :return: Екземпляр класу з балансом 1000.0.
    """
    return BankAccount(1000.0)


def test_deposit(bank_account: BankAccount) -> None:
    """
    Тест поповнення рахунку.
    :param bank_account: Фікстура банківського рахунку.
    """
    bank_account.deposit(500)
    assert bank_account.get_balance() == 1500


def test_withdraw(bank_account: BankAccount) -> None:
    """
    Тест зняття коштів.
    :param bank_account: Фікстура банківського рахунку.
    """
    bank_account.withdraw(700)
    assert bank_account.get_balance() == 300


def test_withdraw_skip(bank_account: BankAccount) -> None:
    """
    Тест із використанням пропуску, якщо рахунок порожній.
    :param bank_account: Фікстура банківського рахунку.
    """
    bank_account.withdraw(1000)
    if bank_account.get_balance() <= 0:
        pytest.skip("Empty wallet!")


@pytest.mark.parametrize("deposit_val, withdraw_val, final_val", [
    (500, 200, 1300),
    (100, 1100, 0),
    (200, 400, 800)
])
def test_bank_params(bank_account: BankAccount, deposit_val: float, withdraw_val: float, final_val: float) -> None:
    """
    Параметризований тест для різних сценаріїв поповнення та зняття.
    :param bank_account: Фікстура банківського рахунку.
    :param deposit_val: Сума поповнення.
    :param withdraw_val: Сума зняття.
    :param final_val: Очікуваний фінальний баланс.
    """
    bank_account.deposit(deposit_val)
    bank_account.withdraw(withdraw_val)
    assert bank_account.get_balance() == final_val


def test_bank_api(bank_account: BankAccount) -> None:
    """
    Тест імітації API через MagicMock для перевірки балансу.
    :param bank_account: Фікстура банківського рахунку.
    """
    bank_account.get_balance = MagicMock(return_value=5000)
    assert bank_account.get_balance() == 5000
