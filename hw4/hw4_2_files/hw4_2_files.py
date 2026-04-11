def avg(file_name) -> None:
    """
    Знаходить середнє арифметичне усіх чисел у файлі file_name, при умові що це числа
    :param file_name: Ім'я файлу
    """
    try:
        numbers = []
        with open(file_name, 'r') as file:
            text = file.read()
        if not text.strip():
            print('File empty!')
            return
        for i in text.split():
            numbers.append(float(i))

        n_sum = sum(numbers)
        n_len = len(numbers)

        print(round(n_sum / n_len, 2))

    except FileNotFoundError:
        print('File not found!')
    except ValueError:
        print('Value error!')


avg('text.txt')
