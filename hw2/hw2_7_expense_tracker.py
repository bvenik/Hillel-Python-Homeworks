total_expense = 0


def add_expense(expense: str) -> None:
    """
    Додає витрату(expense) до total_expense, у випадку помилок при вводі повідомляє про це
    """
    global total_expense
    try:
        value = float(expense)
        if value < 0:
            print("Error: Expense cannot be negative. Use 'Subtract' for corrections.")
            return

        total_expense += value
        print(f"Expense added: {value}. Total expense: {total_expense}")
    except ValueError:
        print(f"Error: '{expense}' is not a valid number. Please enter digits only.")


def subtract_expense(expense: str) -> None:
    """
    Віднімає витрату(expense) від total_expense, у випадку помилок при вводі повідомляє про це
    """
    global total_expense
    try:
        value = float(expense)
        total_expense -= value
        print(f"Expense removed: {value}. Total expense: {total_expense}")
    except ValueError:
        print(f"Error: '{expense}' is not a valid number. Please enter digits only.")


def get_expense() -> None:
    """
    Виводить total expense
    """
    print(f"Total expense: {total_expense}")


def ui() -> None:
    """
    Ініціалізує найпростіший спосіб введення даних користувачем, якщо ввід користувача не є коректним, повідомляє про це
    """
    print("1. Add expense")
    print("2. Subtract expense")
    print("3. Get expense")
    print("4. Exit")
    while True:
        choice = input("Enter your choice: ")
        if choice == "1":
            add_expense(input("Enter expense: "))
        elif choice == "2":
            subtract_expense(input("Enter expense: "))
        elif choice == "3":
            get_expense()
        elif choice == "4":
            break
        else:
            print("Please enter a valid choice")


ui()
