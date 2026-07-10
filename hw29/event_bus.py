import threading
import queue
import time
import fnmatch
from typing import Callable, Any


class EventBus:
    def __init__(self) -> None:
        """
        Initializes the EventBus, internal storage, and background worker thread.
        """
        self.subscribers: dict[str, list[Callable[[Any], None]]] = {}
        self.event_queue: queue.Queue = queue.Queue()
        self.event_log: list[dict[str, Any]] = []

        self.worker_thread: threading.Thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def subscribe(self, event_pattern: str, callback: Callable[[Any], None]) -> None:
        """
        Subscribes a callback function to an event pattern, avoiding duplicates.
        :param event_pattern: name or pattern of the event
        :param callback: callback function to execute
        :return: nothing
        """
        callbacks = self.subscribers.setdefault(event_pattern, [])
        if callback not in callbacks:
            callbacks.append(callback)

    def unsubscribe(self, event_pattern: str, callback: Callable[[Any], None]) -> None:
        """
        Unsubscribes a callback function from an event pattern.
        :param event_pattern: name or pattern of the event
        :param callback: callback function to remove
        :return: nothing
        """
        if event_pattern in self.subscribers:
            if callback in self.subscribers[event_pattern]:
                self.subscribers[event_pattern].remove(callback)

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        Pushes an event to the queue for asynchronous handling.
        :param event_name: direct name of the event being triggered
        :param data: data payload associated with the event
        :return: nothing
        """
        event: dict[str, Any] = {"name": event_name, "data": data, "timestamp": time.time()}
        self.event_log.append(event)
        self.event_queue.put(event)

    def _worker(self) -> None:
        """
        Background loop executing callbacks safely without dropping queue progression.
        :return: nothing
        """
        while True:
            event: dict[str, Any] = self.event_queue.get()
            try:
                event_name: str = event["name"]
                data: Any = event["data"]

                for pattern, callbacks in self.subscribers.items():
                    if fnmatch.fnmatch(event_name, pattern):
                        for callback in callbacks:
                            try:
                                callback(data)
                            except Exception as e:
                                print(f"[ERROR] Worker couldn't do {callback.__name__}: {e}")
            finally:
                self.event_queue.task_done()