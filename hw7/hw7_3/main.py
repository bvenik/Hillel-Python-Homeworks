import csv


def avg_grade(filename: str) -> str:
    """
    Обчислює середню оцінку студентів із CSV-файлу.

    :param filename: Шлях до CSV-файлу.
    :return: Рядок із результатом середньої оцінки.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        total_grades = 0
        count = 0
        for row in reader:
            total_grades += int(row['Оцінка'])
            count += 1
        return f'Average grade: {total_grades / count}'


def add_student(filename: str, st_name: str, st_age: int, st_grade: int | float) -> None:
    """
    Додає новий рядок із даними студента до CSV-файлу.

    :param filename: Шлях до CSV-файлу.
    :param st_name: Ім'я студента.
    :param st_age: Вік студента.
    :param st_grade: Оцінка студента.
    :return: None
    """
    with open(filename, "a", encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Ім'я", "Вік", "Оцінка"])
        writer.writerow({"Ім'я": st_name, 'Вік': st_age, 'Оцінка': st_grade})


add_student('students.csv', 'test', 12, 424)
print(avg_grade('students.csv'))
