#!/usr/bin/python3
"""Heating and door opener."""
import logging
import threading
import time

from lib.doorcontroller import DoorController
from lib.hoovercontroller import HooverController
from lib.plugcontroller import PlugController
from lib.schedule import Schedule
from lib.websocket import WSManager

logging.basicConfig(
    filename="/tmp/shala.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(name=None)

hoover_controller = HooverController(logger)
plug_controller = PlugController(logger)
door_controller = DoorController(logger)
wsm = WSManager(plug_controller, logger)
schedule = Schedule(wsm, logger)


def main_loop():
    """Dont care."""
    old_state = False

    while True:
        schedule.read_settings()
        schedule.check_door_schedule()

        if schedule.check_hoover_schedule():
            hoover_controller.turn_on_hoover()

        new_state = schedule.check_heating_schedule(old_state)

        if new_state is True:
            plug_controller.plug_turn_all_on()
        else:
            plug_controller.plug_turn_all_off()

        wsm.send(str(new_state))
        time.sleep(10)
        old_state = new_state


try:
    thread1 = threading.Thread(target=main_loop, args=())
    thread1.daemon = True
    thread1.start()
    wsm.run()
except Exception as ex:
    print(str(ex))
    pass
