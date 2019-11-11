#!/usr/bin/python
import threading
import logging

import time

from lib.plugcontroller import PlugController
from lib.websocket import WSManager
from lib.schedule import Schedule
from lib.email import Email

logging.basicConfig(filename='/tmp/heating.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
logger = logging.getLogger(name=None)

plug_controller = PlugController(logger)
wsm = WSManager(plug_controller, logger)
schedule = Schedule(wsm, logger)
emailer = Email()

def main_loop():
    heating_state = False

    while True:
        temp_state = heating_state
        heating_state = schedule.check_schedule(heating_state)

        if temp_state != heating_state:
            emailer.send_email("On" if heating_state == True else "Off")

        if heating_state == True:
            plug_controller.plug_turn_all_on()
        else:
            plug_controller.plug_turn_all_off()

        wsm.send(str(heating_state))
        time.sleep(10)

try:
    thread1 = threading.Thread(target=main_loop, args=())
    thread1.daemon = True
    thread1.start()
    wsm.run()
except:
    pass
