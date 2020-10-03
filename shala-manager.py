#!/usr/bin/python3
import threading
import logging

import time

from lib.doorcontroller import DoorController
from lib.plugcontroller import PlugController
from lib.websocket import WSManager
from lib.schedule import Schedule

logging.basicConfig(filename='/tmp/shala.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
logger = logging.getLogger(name=None)

plug_controller = PlugController(logger)
door_controller = DoorController(logger)
wsm = WSManager(plug_controller, logger)
schedule = Schedule(wsm, logger)

def main_loop():
    old_state = False

    while True:
        schedule.read_settings()
        schedule.check_door_schedule()
        
        new_state = schedule.check_heating_schedule(old_state)        

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
