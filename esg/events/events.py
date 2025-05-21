from events.eventbrite import eventbrite_events
from events.adb import adb_events
from events.snp import sp_events
from utils.db_utils import save_events_to_db


def all_events():
    eventbrite = eventbrite_events()
    adb = adb_events()
    sp = sp_events()

    all_events = []

    all_events.extend(eventbrite)
    print(f"Total events after adding Eventbrite events: {len(all_events)}")
        
    all_events.extend(adb)
    print(f"Total events after adding ADB events: {len(all_events)}")
        
    all_events.extend(sp)
    print(f"Total events after adding S&P events: {len(all_events)}")

    save_events_to_db(all_events, also_save_csv=True, filename="test_events.csv")