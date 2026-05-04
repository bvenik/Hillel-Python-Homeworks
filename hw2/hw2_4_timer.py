default_time = 60


def training_session(rounds: int) -> int:
    """
    Функція training_session, яка приймає rounds, шляхом обчислень та використанню вкладеної функції adjust_time виводить час усіх раундів вказаних користувачем
    """
    time_per_round = default_time + 5

    def adjust_time():
        """
        Службова функція для training_session, відповідає за те, на скільки буде зменшуватись значення time_per_round при кожному наступному раунді (rounds)
        """
        nonlocal time_per_round
        time_per_round -= 5

    for i in range(1, rounds + 1):
        if time_per_round == 0:
            break
        else:
            adjust_time()
            print(f"Раунд {i}: {time_per_round} хвилин")

    return time_per_round


training_session(3)
