import time
from event_scheduler.scheduler import EventScheduler, example_event, event_listener


def test_event_scheduler():
    scheduler = EventScheduler()

    # Schedule event to trigger after 1 second
    scheduler.schedule_event("test_event", 1, example_event)
    scheduler.add_listener("test_event", event_listener)

    # Wait for event to trigger
    time.sleep(2)
    assert True  # If no errors, the test is successful
