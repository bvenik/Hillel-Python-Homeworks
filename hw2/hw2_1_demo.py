import builtins

numbers = [2, 7, 4, 7, 1, 4, 3]


# Спосіб 1, згідно з умовою

def my_sum():
    def sum():
        return "This is my custom sum function!"

    return sum()


print(my_sum())
print(sum(numbers))


# Спосіб 2

def sum(x):
    return "This is my custom sum function!"


print(sum(numbers))
print(builtins.sum(numbers))

# Відповідь на перше питання - вона, за правилом-послідовністю Local->Enclosed->Global->Built-in перекриває собою минулу, вбудовану функцію, тому при виклику будуть виконуватись вже не вбудовані дії, а прописані користувачем дії
# Відповідь на друге питання - імпортувати & використати модуль builtins
