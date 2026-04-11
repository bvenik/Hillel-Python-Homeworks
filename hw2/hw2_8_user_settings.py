def create_user_settings() -> tuple:
    """
    Створює замикання для збереження налаштувань користувача у внутрішньому словнику settings.
    """
    settings = {
        "theme": "light",
        "language": "ua",
        "notifications": True
    }

    def edit_settings(key: str, value) -> None:
        """
        Змінює конкретний параметр налаштувань за ключем.
        """
        if key in settings:
            settings[key] = value
            print(f"Налаштування '{key}' змінено на: {value}")
        else:
            print(f"Помилка: Параметр '{key}' не існує.")

    def get_settings() -> None:
        """
        Виводить поточний стан усіх налаштувань.
        """
        for key, value in settings.items():
            print(f"{key.capitalize()}: {value}")

    return edit_settings, get_settings


edit_stg, get_stg = create_user_settings()
edit_stg("theme", "dark")
edit_stg("language", "en")
edit_stg("notifications", False)
edit_stg("unknown", 14)
get_stg()
