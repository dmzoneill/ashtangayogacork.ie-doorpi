#!/usr/bin/python3
"""Dont care."""
import threading
import time
from os.path import isfile

import RPi.GPIO as Gpio


from websocket_server import WebsocketServer


class DoorController:
    """Dont care."""

    logger = None

    server = None
    wsport = 9001

    buzzer_input = 12
    door_release_output = 20
    buzzer_event_completed = True
    last_time = time.time()

    def __init__(self, logger):
        """Dont care."""
        self.last_time = time.time()
        self.logger = logger
        self.logger.debug("Started door controller")
        self.gpio_setup()
        thread1 = threading.Thread(target=self.websocket_setup, args=())
        thread1.daemon = True
        thread1.start()

    def gpio_setup(self):
        """Dont care."""
        Gpio.setmode(Gpio.BCM)
        Gpio.setup(self.buzzer_input, Gpio.IN)
        Gpio.setup(self.door_release_output, Gpio.OUT)
        Gpio.add_event_detect(
                self.buzzer_input, Gpio.BOTH, callback=self.buzzer_handler
        )
        channel_is_on = Gpio.input(self.buzzer_input)
        print(str(channel_is_on))
        self.logger.info("Door Gpio setup complete")

    def websocket_setup(self):
        """Dont care."""
        self.server = WebsocketServer(self.wsport, host="0.0.0.0")
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.msg_received)
        self.logger.info("Door WebsocketServer setup complete")
        self.server.run_forever()

    def buzzer_handler(self, pin):
        print("here pin change")
        """Dont care."""
        self.open_door()

    def client_left(self, cl, server):
        """Dont care."""
        try:
            self.logger.info("Door Client (%s) left" % cl["id"])
        except Exception as ex:
            self.logger.error("Door failed disconnect")
            self.logger.error(str(ex))

    def new_client(self, cl, server):
        """Dont care."""
        try:
            self.logger.info("Door New client (%s) connected" % cl["id"])
        except Exception as ex:
            self.logger.error("Door failed connect")
            self.logger.error(str(ex))

    def msg_received(self, cl, server, msg):
        """Dont care."""
        if "refresh" in msg:
            self.logger.info(msg)
            self.server.send_message_to_all(msg)
            return
        self.logger.info("Door Client (%s) : %s" % (cl["id"], msg))
        self.open_door()

    def open_door(self):
        channel_is_on = Gpio.input(self.buzzer_input)
        print(str(channel_is_on))
        """Dont care."""
        Gpio.output(self.door_release_output, False)
        self.server.send_message_to_all(str(False))
        print("here open_door 1988")
        if self.last_time + 5 > time.time():
            self.last_time = time.time()
            print("too fast")
            return False

        if isfile("/var/www/html/scratch/enabled") is False:
            print("here door not enabled")
            Gpio.output(self.door_release_output, False)
            self.last_time = time.time()
            return False
        print("here door open 2")

        Gpio.output(self.door_release_output, True)
        self.server.send_message_to_all(str(True))
        time.sleep(0.5)
        Gpio.output(self.door_release_output, False)
        self.server.send_message_to_all(str(False))
        self.last_time = time.time()
        return True
