class MessageSender:
    """Абстрактний клас, що визначає інтерфейс для відправки повідомлень."""

    def send_message(self, message: str) -> None:
        """Відправляє повідомлення через конкретний канал зв'язку."""
        pass


class SMSService:
    """Сервіс для роботи з SMS-повідомленнями."""

    def send_sms(self, phone_number: str, message: str) -> None:
        """Виконує безпосередню відправку SMS на вказаний номер."""
        print(f"Успішна відправка SMS на {phone_number}: {message}")


class EmailService:
    """Сервіс для роботи з електронною поштою."""

    def send_email(self, email_address: str, message: str) -> None:
        """Виконує безпосередню відправку Email на вказану адресу."""
        print(f"Успішна відправка Email на {email_address}: {message}")


class PushService:
    """Сервіс для роботи з Push-сповіщеннями."""

    def send_push(self, device_id: str, message: str) -> None:
        """Виконує безпосередню відправку Push-повідомлення на пристрій."""
        print(f"Успішна відправка Push-повідомлення на пристрій {device_id}: {message}")


class SMSAdapter(MessageSender):
    """Адаптер для інтеграції SMSService з інтерфейсом MessageSender."""

    def __init__(self, sms_service: SMSService, phone_number: str) -> None:
        """Ініціалізує адаптер сервісом SMS та номером телефону отримувача."""
        self.sms_service = sms_service
        self.phone_number = phone_number

    def send_message(self, message: str) -> None:
        """Валідує номер та відправляє повідомлення через SMSService."""
        try:
            if self.phone_number.startswith('+') and self.phone_number.count('+') == 1 and self.phone_number[
                1:].isdigit():
                self.sms_service.send_sms(self.phone_number, message)
            else:
                raise ValueError(f"Некоректний формат номеру: {self.phone_number}")
        except Exception as e:
            print(f"[SMS ERROR]: {e}")


class EmailAdapter(MessageSender):
    """Адаптер для інтеграції EmailService з інтерфейсом MessageSender."""

    def __init__(self, email_service: EmailService, email_address: str) -> None:
        """Ініціалізує адаптер сервісом Email та адресою отримувача."""
        self.email_service = email_service
        self.email_address = email_address

    def send_message(self, message: str) -> None:
        """Валідує адресу та відправляє повідомлення через EmailService."""
        try:
            if self.email_address.count('@') == 1 and "." in self.email_address:
                self.email_service.send_email(self.email_address, message)
            else:
                raise ValueError(f"Некоректний формат пошти: {self.email_address}")
        except Exception as e:
            print(f"[EMAIL ERROR]: {e}")


class PushAdapter(MessageSender):
    """Адаптер для інтеграції PushService з інтерфейсом MessageSender."""

    def __init__(self, push_service: PushService, device_id: str) -> None:
        """Ініціалізує адаптер сервісом Push та ID пристрою."""
        self.push_service = push_service
        self.device_id = device_id

    def send_message(self, message: str) -> None:
        """Перевіряє наявність ID та відправляє Push-повідомлення."""
        try:
            if self.device_id:
                self.push_service.send_push(self.device_id, message)
            else:
                raise ValueError("Device ID порожній")
        except Exception as e:
            print(f"[PUSH ERROR]: {e}")


def strange_test_function() -> None:
    """Виконує масову розсилку через поточний набір адаптерів."""
    senders = [sms_adapter, email_adapter, push_adapter]
    for sender in senders:
        sender.send_message(message)


sms_service = SMSService()
email_service = EmailService()
push_service = PushService()

message = "Привіт! Це тестове повідомлення."

sms_adapter = SMSAdapter(sms_service, "+380123456789")
email_adapter = EmailAdapter(email_service, "user@example.com")
push_adapter = PushAdapter(push_service, "device123")

strange_test_function()

sms_adapter = SMSAdapter(sms_service, "++80123456789")
email_adapter = EmailAdapter(email_service, "userexample.com")
push_adapter = PushAdapter(push_service, "")

strange_test_function()
