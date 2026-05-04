class UnknownOperationError(Exception):
    pass


def calculation() -> None:
    """
    Функція calculation() відповідає за звичні функції калькулятора (+ - * / ^), при помилках викликає exception різних видів, зациклений, допоки користувач не напише 'exit' у полі operator
    """
    res = ''
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            operator = input("Enter operator: ")

            if operator not in ['+', '-', '*', '/', '**', '^', 'exit']:
                raise UnknownOperationError(f"Операція '{operator}' не підтримується.")

            if operator == '+':
                res = num1 + num2

            elif operator == '-':
                res = num1 - num2

            elif operator == '*':
                res = num1 * num2

            elif operator == '/':
                if num2 == 0:
                    raise ZeroDivisionError()
                else:
                    res = num1 / num2

            elif operator == '**':
                res = num1 ** num2

            elif operator == '^':
                res = num1 ** num2

            elif operator == 'exit':
                print("Bye bye")
                raise SystemExit()

            if res == int(res):
                print(f"Result: {int(res)}")
            else:
                print(f"Result: {round(float(res), 4)}")

        except ZeroDivisionError:
            print("Error, division by zero")
        except ValueError:
            print("Error, invalid value")
        except UnknownOperationError:
            print("Error, invalid operator")
        except OverflowError:
            print("Error, overflow")


calculation()
