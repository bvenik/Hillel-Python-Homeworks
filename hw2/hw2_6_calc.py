def create_calculator(operator: str):
    """
    Ініціалізує функцію create_calculator з вбудованими в вкладену функцію calculation математичними операторами
    """

    def calculation(num1: int | float, num2: int | float) -> int | float | str:
        """
        Приймає 1 число (num1) та 2 число (num2) для майбутніх математичних операцій (+ - * / ^), у випадку помилки ділення, чи некоректного оператора сповіщає про це
        """
        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            if num2 == 0:
                return "Error, division by zero"
            else:
                return num1 / num2
        elif operator == '^':
            return num1 ** num2
        else:
            return "Error, invalid/unknown operator"

    return calculation


add = create_calculator('+')
sub = create_calculator('-')
mul = create_calculator('*')
div = create_calculator('/')
pwr = create_calculator('^')
unknown = create_calculator('&')

print(add(4, 32))
print(sub(80, 76))
print(mul(12, 7))
print(div(2, 4))
print(div(53, 0))
print(pwr(7, 3))
print(unknown(7, 3))
