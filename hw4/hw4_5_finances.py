class InsufficientFundsException(Exception):
    def __init__(self, required_amount: float, current_balance: float, currency: str = "USD",
                 transaction_type: str = "purchase") -> None:
        """
        Ініціалізує помилку нестачі коштів на рахунку
        :param required_amount: сума, яку треба сплатити
        :param current_balance: поточний залишок
        :param currency: валюта
        :param transaction_type: тип операції
        """
        self.required_amount = required_amount
        self.current_balance = current_balance
        self.currency = currency
        self.transaction_type = transaction_type


def process_transaction(amount: float, balance: float, t_type: str = "withdrawal") -> None:
    """
    Перевіряє баланс та проводить транзакцію
    :param amount: необхідна сума
    :param balance: поточний баланс
    :param t_type: тип транзакції
    """
    if balance < amount:
        raise InsufficientFundsException(amount, balance, "UAH", t_type)
    print(f"Transaction {t_type} successful! New balance: {balance - amount}")


try:
    process_transaction(1500.0, 500.0, "purchase")
except InsufficientFundsException as e:
    missing = e.required_amount - e.current_balance
    print(f"Operation: {e.transaction_type}")
    print(f"Insufficient funds: {missing} {e.currency} more needed.")
    print("Operation cancelled.")
