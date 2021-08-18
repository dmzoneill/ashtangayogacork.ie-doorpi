#!/usr/bin/python3
"""Heating and door opener."""
import logging
import requests
import time

from lib.schedule import Schedule

logging.basicConfig(
    filename="/tmp/shala.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(name=None)
schedule = Schedule(logger)


def heater_change_state(state):
    uri = "on" if state else "off"
    r =requests.get('http://127.0.0.1:8000/' + uri)
    print(r.content)


def main():
    """Dont care."""
    old_state = False

    while True:
        schedule.read_settings()
        schedule.check_door_schedule()

        new_state = schedule.check_heating_schedule(old_state)
        try:
            heater_change_state(new_state)
        except:
            pass

        time.sleep(3)
        old_state = new_state


if __name__ == "__main__":
    main()