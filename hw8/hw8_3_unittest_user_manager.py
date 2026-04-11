from typing import List, Dict, Any
import pytest


class UserManager:
    """
    Клас для керування списком користувачів.
    """

    def __init__(self) -> None:
        """
        Ініціалізація порожнього списку користувачів.
        """
        self.current_users: List[Dict[str, Any]] = []

    def add_user(self, name: str, age: int) -> None:
        """
        Додає нового користувача до списку.
        :param name: ім'я користувача
        :param age: вік користувача
        :return: None
        """
        self.current_users.append({'name': name, 'age': age})

    def remove_user(self, name: str) -> None:
        """
        Видаляє користувача зі списку за його ім'ям.
        :param name: ім'я користувача для видалення
        :return: None
        """
        self.current_users = [user for user in self.current_users if user['name'] != name]

    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Повертає повний список поточних користувачів.
        :return: список словників з даними користувачів
        """
        return self.current_users


@pytest.fixture
def user_manager() -> UserManager:
    """
    Фікстура для створення екземпляра UserManager з початковими даними.
    :return: налаштований об'єкт UserManager
    """
    um = UserManager()
    um.add_user("Alice", 30)
    um.add_user("Bob", 25)
    return um


class TestUserManager:
    """
    Набір модульних тестів для перевірки функціональності класу UserManager.
    """

    def test_add_user(self, user_manager: UserManager) -> None:
        """
        Тестування успішного додавання нового користувача.
        :param user_manager: фікстура менеджера користувачів
        :return: None
        """
        user_manager.add_user("Cat", 15)
        assert user_manager.get_all_users() == [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25},
                                                {'name': 'Cat', 'age': 15}]

    def test_remove_user(self, user_manager: UserManager) -> None:
        """
        Тестування видалення користувача, що існує та ігнорування відсутнього.
        :param user_manager: фікстура менеджера користувачів
        :return: None
        """
        user_manager.remove_user("Bob")
        user_manager.remove_user("Guest")
        assert user_manager.get_all_users() == [{'name': 'Alice', 'age': 30}]

    def test_get_all_users(self, user_manager: UserManager) -> None:
        """
        Тестування отримання списку всіх користувачів без змін.
        :param user_manager: фікстура менеджера користувачів
        :return: None
        """
        expected = [{'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}]
        assert user_manager.get_all_users() == expected

    def test_skip_user(self, user_manager: UserManager) -> None:
        """
        Тест, що пропускається, якщо кількість користувачів менша або дорівнює трьом.
        :param user_manager: фікстура менеджера користувачів
        :return: None
        """
        users = user_manager.get_all_users()
        if len(users) <= 3:
            pytest.skip("'Users' count is less than 3")
