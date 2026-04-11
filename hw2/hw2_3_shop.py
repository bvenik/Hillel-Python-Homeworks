discount = 0.1


def create_order(price: int | float, add_discount: int | float) -> int | float:
    """
    Створює початкову ціну для товару, та першочергово віднімає від неї знижку, вказану глобально. Далі, у випадку якщо вказано додаткову знижку, віднімає її теж від вже модифікованої вартості (apply_additional_discount). Далі повертає повний, кінцевий результат
    :param price: початкова ціна товару
    :param add_discount: додаткова знижка (вкладена функція apply_additional_discount)
    :return: ціна товару з урахуванням двох видів знижок
    """
    final_price = price - price * discount

    def apply_additional_discount(*args) -> None:
        """
        Функція відповідає за додаткову знижку, спочатку обчислює ціну зі звичайною знижкою, і далі від цієї вартості віднімає додаткову знижку, яка вказується користувачем індивідуально
        """
        nonlocal final_price
        final_price = final_price - final_price * add_discount

    apply_additional_discount()
    return round(final_price, 2)


# create_order(1000)  # Початкова ціна: 1000, кінцева ціна зі знижкою 10%: 900
print(create_order(1000, 0.2))
print(create_order(1000, 0))
