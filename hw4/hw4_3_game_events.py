class GameEventException(Exception):
    def __init__(self, event_type: str, details: dict) -> None:
        """
        Ініціалізує клас-виняток
        :param event_type: тип події (levelUp або death)
        :param details: обставини, додаток до event_type
        """
        self.event_type = event_type
        self.details = details


def game_event(action: str) -> None:
    if action == "Victory":
        raise GameEventException("levelUp", {"level": 3, "gained_xp": 800})
    elif action == "Fall":
        raise GameEventException("death", {"how": "fall", "gained_dmg": 100})


try:
    # game_event("Victory")
    game_event("Fall")
except GameEventException as e:
    if e.event_type == 'levelUp':
        print(f"You gained {e.details['gained_xp']} xp. Your level is {e.details['level']}")
    elif e.event_type == 'death':
        print(f"You died because of {e.details['how']}. You lost {e.details['gained_dmg']} health")
