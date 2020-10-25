#!/usr/bin/python
"""Dont care."""
from datetime import datetime, timedelta

from websocket_server import WebsocketServer


class WSManager:
    """Dont care."""

    plug_controller = None
    server = WebsocketServer(9002, host="0.0.0.0")
    logger = None
    boost_time = None

    def __init__(self, plug_controller, logger):
        """Dont care."""
        self.plug_controller = plug_controller
        self.logger = logger
        self.logger.debug("started")

    def client_left(self, cl, server):
        """Dont care."""
        msg = "Client (%s) left" % cl["id"]
        self.logger.debug(msg)

    def new_client(self, cl, server):
        """Dont care."""
        msg = "New client (%s) connected" % cl["id"]
        self.logger.debug(msg)

    def msg_received(self, cl, server, msg):
        """Dont care."""
        msg = "Client (%s) : %s" % (cl["id"], msg)
        if self.boost_time is None:
            self.boost_time = datetime.now() + timedelta(minutes=15)
            self.plug_controller.plug_turn_all_on()
        else:
            self.boost_time = None
            self.plug_controller.plug_turn_all_off()

        self.logger.debug(msg)

    def send(self, msg):
        """Dont care."""
        try:
            self.logger.debug("Send: " + msg)
            self.server.send_message_to_all(msg)
        except Exception as ex:
            self.logger.debug(str(ex))
            pass

    def get_boost_time(self):
        """Dont care."""
        return self.boost_time

    def set_boost_time(self, boost):
        """Dont care."""
        self.boost_time = boost

    def run(self):
        """Dont care."""
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.msg_received)
        self.server.run_forever()
