events = []


def event_calendar():
    """
    Ініціалізація глобальної функції event_calendar та її вкладених функцій add_event, remove_event, show_events
    """

    def add_event(event: str, date: str) -> None:
        """
        Додає подію(event) до списку(events) на дату(date), за умови відсутності такої пари у списку
        """
        if [event, date] in events:
            print(f"{event} already scheduled on {date}")
        else:
            events.append([event, date])
            print(f"{event} added to calendar on {date}")

    def remove_event(event: str, date: str) -> None:
        """
        Видаляє подію(event) та дату(date) зі списку(events), якщо вони там існують
        """
        if [event, date] in events:
            events.remove([event, date])
            print(f"{event} on {date} removed from calendar")
        else:
            print(f"{event} is not in calendar on {date}")

    def show_events() -> None:
        """
        Виводить усі заплановані події та їх дати із глобального списку events
        """
        print('\n')
        for [event, date] in events:
            print(f"{event} on {date}")
        print('\n')

    return add_event, remove_event, show_events


calendar_add, calendar_remove, calendar_show = event_calendar()

calendar_add("Gym", "01-03-2027")
calendar_add("Gym", "01-03-2027")
calendar_remove("Gym", "01-03-2027")
calendar_remove("Gym", "04-05-2027")
calendar_add("Fishing Time", "05-03-2026")
calendar_add("Cooking Time", "05-03-2026")
calendar_show()
