import time
from threading import Timer


class EventScheduler:
    def __init__(self):
        self.events = []
        self.listeners = {}

    def schedule_event(self, event_name, delay, callback):
        """Schedules an event after a certain delay."""
        timer = Timer(delay, self._trigger_event, [event_name])
        timer.start()
        self.events.append((event_name, callback))

    def add_listener(self, event_name, listener):
        """Adds a listener for a specific event."""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(listener)

    def _trigger_event(self, event_name):
        """Triggers an event and notifies all listeners."""
        for event, callback in self.events:
            if event == event_name:
                callback()
                if event_name in self.listeners:
                    for listener in self.listeners[event_name]:
                        listener()


# Example event callback
def example_event():
    print("Event Triggered!")


# Example listener
def event_listener():
    print("Listener Notified!")
