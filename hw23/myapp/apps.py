from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self) -> None:
        """
        Loads signal receivers when the application starts.
        :return: nothing
        """
        from . import signals

