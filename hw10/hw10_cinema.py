import sqlite3
from datetime import datetime
import time


def movie_age(release_year: int) -> int:
    """
    Обчислює кількість років, що минули з моменту виходу фільму.
    :param release_year: Рік випуску фільму.
    :return: Різниця між поточним роком та роком випуску.
    """
    current_year: int = datetime.now().year
    return current_year - release_year


def init_db() -> sqlite3.Connection:
    """
    Ініціалізує підключення до бази даних та створює необхідні таблиці.
    :return: Об'єкт підключення до SQLite.
    """
    conn: sqlite3.Connection = sqlite3.connect('cinema.db')
    conn.create_function("movie_age", 1, movie_age)
    cursor: sqlite3.Cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS movies
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       title
                       TEXT
                       NOT
                       NULL,
                       release_year
                       INTEGER,
                       genre
                       TEXT
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS actors
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       birth_year
                       INTEGER
                   )
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS movie_cast
                   (
                       movie_id
                       INTEGER,
                       actor_id
                       INTEGER,
                       PRIMARY
                       KEY
                   (
                       movie_id,
                       actor_id
                   ),
                       FOREIGN KEY
                   (
                       movie_id
                   ) REFERENCES movies
                   (
                       id
                   ),
                       FOREIGN KEY
                   (
                       actor_id
                   ) REFERENCES actors
                   (
                       id
                   )
                       )
                   ''')

    conn.commit()
    return conn


def add_movie(cursor: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    """
    Додає новий фільм до бази даних через консольне введення.
    :param cursor: Курсор бази даних.
    :param conn: Об'єкт підключення для збереження змін.
    """
    title: str = input("Назва фільму: ")
    try:
        year: int = int(input("Рік випуску: "))
    except ValueError:
        print("Помилка! Будь ласка, введіть число.")
        return
    genre: str = input("Жанр: ")
    cursor.execute("INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)", (title, year, genre))
    conn.commit()
    print(f"Фільм {title} ({year}) додано")


def add_actor(cursor: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    """
    Додає нового актора до бази даних через консольне введення.
    :param cursor: Курсор бази даних.
    :param conn: Об'єкт підключення для збереження змін.
    """
    name: str = input("Призвіще та ім'я: ")
    try:
        birth_year: int = int(input("Введіть рік народження актора: "))
    except ValueError:
        print("Помилка! Будь ласка, введіть число.")
        return
    cursor.execute("INSERT INTO actors (name, birth_year) VALUES (?, ?)", (name, birth_year))
    conn.commit()
    print(f"Актор {name} успішно доданий/а")


def show_all_with_actors(cursor: sqlite3.Cursor) -> None:
    """
    Виводить список усіх фільмів та імена акторів, що в них знімалися.
    :param cursor: Курсор бази даних.
    """
    query: str = '''
                 SELECT m.title, GROUP_CONCAT(a.name, ', ')
                 FROM movies m
                          INNER JOIN movie_cast mc ON m.id = mc.movie_id
                          INNER JOIN actors a ON a.id = mc.actor_id
                 GROUP BY m.title \
                 '''
    cursor.execute(query)
    for row in cursor.fetchall():
        print(f"Фільм: '{row[0]}', Актори: {row[1]}")


def show_unique_genres(cursor: sqlite3.Cursor) -> None:
    """
    Виводить список унікальних жанрів фільмів без повторень.
    :param cursor: Курсор бази даних.
    """
    cursor.execute("SELECT DISTINCT genre FROM movies")
    print("\n--- Унікальні жанри ---")
    for row in cursor.fetchall():
        print(f"- {row[0]}")


def count_by_genre(cursor: sqlite3.Cursor) -> None:
    """
    Виводить кількість фільмів, закріплених за кожним жанром.
    :param cursor: Курсор бази даних.
    """
    cursor.execute("SELECT genre, COUNT(*) FROM movies GROUP BY genre")
    print("\n--- Кількість фільмів за жанром ---")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")


def avg_actor_birth_year_by_genre(cursor: sqlite3.Cursor) -> None:
    """
    Знаходить середній рік народження акторів у фільмах вказаного жанру.
    :param cursor: Курсор бази даних.
    """
    genre: str = input("Введіть жанр для розрахунку: ")
    query: str = '''
                 SELECT AVG(a.birth_year)
                 FROM actors a
                          JOIN movie_cast mc ON a.id = mc.actor_id
                          JOIN movies m ON m.id = mc.movie_id
                 WHERE m.genre LIKE ? \
                 '''
    cursor.execute(query, (f'%{genre}%',))
    result: tuple = cursor.fetchone()
    if result and result[0]:
        print(f"Середній рік народження акторів у жанрі '{genre}': {int(result[0])}")
    else:
        print("Для цього жанру немає даних.")


def search_by_title(cursor: sqlite3.Cursor) -> None:
    """
    Виконує пошук фільму за ключовим словом у назві.
    :param cursor: Курсор бази даних.
    """
    keyword: str = input("Введіть слово для пошуку: ")
    cursor.execute("SELECT title, release_year FROM movies WHERE title LIKE ?", (f'%{keyword}%',))
    results: list = cursor.fetchall()
    for row in results:
        print(f"Знайдено: {row[0]} ({row[1]})")


def show_movies_paginated(cursor: sqlite3.Cursor) -> None:
    """
    Виводить список фільмів частинами (пагінація) через LIMIT та OFFSET.
    :param cursor: Курсор бази даних.
    """
    limit: int = 3
    offset: int = 0
    while True:
        cursor.execute("SELECT title FROM movies LIMIT ? OFFSET ?", (limit, offset))
        movies: list = cursor.fetchall()
        if not movies:
            print("Більше фільмів немає.")
            break

        print(f"\n--- Сторінка (зміщення {offset}) ---")
        for row in movies:
            print(f"- {row[0]}")

        cont: str = input("\nПоказати наступні 3? (y/n): ")
        if cont.lower() == 'y':
            offset += limit
        else:
            break


def show_all_names_union(cursor: sqlite3.Cursor) -> None:
    """
    Виводить об'єднаний список назв фільмів та імен акторів.
    :param cursor: Курсор бази даних.
    """
    query: str = "SELECT title AS name FROM movies UNION SELECT name FROM actors"
    cursor.execute(query)
    print("\n--- Усі назви та імена ---")
    for row in cursor.fetchall():
        print(f"{row[0]}")


def show_movie_ages(cursor: sqlite3.Cursor) -> None:
    """
    Виводить список фільмів та кількість років з моменту їх виходу.
    :param cursor: Курсор бази даних.
    """
    cursor.execute("SELECT title, movie_age(release_year) FROM movies")
    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")


def link_actor_to_movie(cursor: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    """
    Зв'язує актора із фільмом у таблиці movie_cast.
    :param cursor: Курсор бази даних.
    :param conn: Об'єкт підключення для збереження змін.
    """
    cursor.execute("SELECT id, name FROM actors")
    actors: list = cursor.fetchall()
    for row in actors:
        print(f"ID: {row[0]}. Ім'я: {row[1]}")
    try:
        actor_id: int = int(input("Введіть ID актора: "))
        cursor.execute("SELECT id, title FROM movies")
        movies: list = cursor.fetchall()
        for row in movies:
            print(f"ID: {row[0]}. Ім'я: {row[1]}")
        movie_id: int = int(input("Введіть ID фільму: "))
    except ValueError:
        print("Помилка! ID має бути числом.")
        return

    cursor.execute("INSERT OR IGNORE INTO movie_cast (movie_id, actor_id) VALUES (?, ?)", (movie_id, actor_id))
    conn.commit()
    print(f"Актор успішно доданий/а до фільму")


def main() -> None:
    """
    Головна функція, що забезпечує роботу консольного меню застосунку.
    """
    conn: sqlite3.Connection = init_db()
    cursor: sqlite3.Cursor = conn.cursor()

    while True:
        time.sleep(0.5)
        print("\n--- КІНОБАЗА ---")
        print("1. Додати фільм")
        print("2. Додати актора")
        print("3. Показати всі фільми з акторами")
        print("4. Показати унікальні жанри")
        print("5. Показати кількість фільмів за жанром")
        print("6. Середній рік народження акторів за жанром")
        print("7. Пошук фільму за назвою")
        print("8. Показати фільми (Пагінація)")
        print("9. Усі актори та назви")
        print("10. Показати вік фільмів")
        print("11. Додати актора до складу фільму")
        print("0. Вихід")

        choice: str = input("\nВиберіть дію: ")

        if choice == '1':
            add_movie(cursor, conn)
        elif choice == '2':
            add_actor(cursor, conn)
        elif choice == '3':
            show_all_with_actors(cursor)
        elif choice == '4':
            show_unique_genres(cursor)
        elif choice == '5':
            count_by_genre(cursor)
        elif choice == '6':
            avg_actor_birth_year_by_genre(cursor)
        elif choice == '7':
            search_by_title(cursor)
        elif choice == '8':
            show_movies_paginated(cursor)
        elif choice == '9':
            show_all_names_union(cursor)
        elif choice == '10':
            show_movie_ages(cursor)
        elif choice == '11':
            link_actor_to_movie(cursor, conn)
        elif choice == '0':
            break

    conn.close()


if __name__ == "__main__":
    main()
