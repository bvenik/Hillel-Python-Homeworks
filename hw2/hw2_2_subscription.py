subscribers = []


def subscribe(name: str) -> str:
    """
    1. Додає name до списку subscribers
    2. Викликає функцію confirm_subscription
    """
    subscribers.append(name)

    def confirm_subscription() -> str:
        """
        Викликає текст про успішне додавання name до списку subscribers
        """
        return f"Підписка підтверджена для {name}"

    return confirm_subscription()


def unsubscribe(name: str) -> str:
    """
    Прибирає name зі списку list
    Умова 1 - Якщо name був у списку list, то виводиться відповідний текст
    Умова 2 - Якщо name не був у списку list, то виводиться відповідний текст
    """
    if name in subscribers:
        subscribers.remove(name)
        return f"Підписка скасована для {name}"
    else:
        return f"{name} не є підписаним"


subscribe("Олена")
subscribe("Ігор")
print(subscribers)  # ['Олена', 'Ігор']
print(unsubscribe("Ігор"))  # 'Ігор успішно відписаний'
print(unsubscribe("Дмитро"))  # Хто це?
print(subscribers)  # ['Олена']
