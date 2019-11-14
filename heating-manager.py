#!/usr/bin/python
import threading
import logging

import time

from lib.plugcontroller import PlugController
from lib.websocket import WSManager
from lib.schedule import Schedule

logging.basicConfig(filename='/tmp/heating.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
logger = logging.getLogger(name=None)

plug_controller = PlugController(logger)
wsm = WSManager(plug_controller, logger)
schedule = Schedule(wsm, logger)

def main_loop():
    old_state = False

    while True:
        new_state = schedule.check_schedule(old_state)

        if new_state == True:
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
except:
    pass
