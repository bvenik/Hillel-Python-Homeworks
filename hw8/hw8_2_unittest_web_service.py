import unittest
from unittest.mock import MagicMock, patch
import requests


class WebService:
    """
    Клас для взаємодії з зовнішніми вебсторінками та отримання даних.
    """

    def get_data(self, url: str) -> dict:
        """
        Виконує GET-запит до вказаного URL та обробляє відповідь.
        :param url: посилання на вебсторінку
        :return: словник із JSON-даними або повідомленням про помилку
        """
        try:
            response: requests.Response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            return {"error": str(err)}


class TestWebService(unittest.TestCase):
    """
    Набір модульних тестів для класу WebService з використанням мокування
    """

    def setUp(self) -> None:
        """
        Налаштування екземпляра WebService перед кожним тестом
        :return: None
        """
        self.service: WebService = WebService()

    @patch('requests.get')
    def test_returned(self, mock_get: MagicMock) -> None:
        """
        Тестування успішного отримання даних від сервера.
        :param mock_get: мок-об'єкт для підміни методу requests.get
        :return: None
        """
        unreal_response: MagicMock = MagicMock()
        unreal_response.json.return_value = {"data": "test"}
        mock_get.return_value = unreal_response
        result = self.service.get_data('https://quotes.toscrape.com/')
        self.assertEqual(result, {"data": "test"})
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_not_found(self, mock_get: MagicMock) -> None:
        """
        Тестування обробки HTTP помилок (наприклад 404)
        :param mock_get: мок-об'єкт для підміни методу requests.get
        :return: None
        """
        unreal_response: MagicMock = MagicMock()
        unreal_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error")
        mock_get.return_value = unreal_response
        result = self.service.get_data('https://quotes.toscrape.com/')
        self.assertIn("error", result)


if __name__ == '__main__':
    unittest.main()
