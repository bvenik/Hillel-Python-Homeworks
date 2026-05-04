class User:
    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        """
        Ініціалізація користувача
        :param first_name: ім'я
        :param last_name: прізвище
        :param email: електронна пошта
        """
        self._first_name = ""
        self._last_name = ""
        self._email = ""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    @property
    def first_name(self) -> str:
        """Повертає ім'я користувача"""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """Встановлює ім'я, якщо воно не порожнє"""
        if len(value) > 0:
            self._first_name = value
        else:
            print("Please enter a valid first name!")

    @property
    def last_name(self) -> str:
        """Повертає прізвище користувача"""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """Встановлює прізвище, якщо воно не порожнє"""
        if len(value) > 0:
            self._last_name = value
        else:
            print("Please enter a valid last name!")

    @property
    def email(self) -> str:
        """Повертає пошту(email) користувача"""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """
        Перевіряє формат email перед встановленням на вміст '@' та хоча б одну '.'
        """
        if "@" in value and "." in value:
            self._email = value
        else:
            print(f"Invalid email format: {value}")
            self._email = "Invalid email or email format!"

    def __repr__(self) -> str:
        """Рядкове представлення об'єкта користувача"""
        return f"Name: {self.first_name}, Lastname: {self.last_name}, Email: {self.email}"


user = User("John", "Doe", "jdoe@gmail.com")
print(user)
user.email = "jdoegmailcom"
print(f"Current email: {user.email}")
