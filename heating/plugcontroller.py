#!/usr/bin/python3
"""Dont care."""
import sys
import time
import logging
from PyP100 import PyP100


logging.basicConfig(level=logging.INFO)


class PlugController:
    """Dont care."""

    plugs = ["192.168.8.20", "192.168.8.30", "192.168.8.40", "192.168.8.50"]
    retries = 3
    username = None
    password = None

    def __init__(self):
        """Dont care."""
        f = open("/creds","r")
        lines = f.readlines()
        self.username = lines[0].strip()
        self.password = lines[1].strip()
        f.close()
        logging.info("started plug controller")

    def plug_turn_all_off(self):
        """Dont care."""
        logging.info("plug_turn_all_off")
        for plug_ip in self.plugs:
            self.plug_turn_off(plug_ip)

    def plug_turn_all_on(self):
        """Dont care."""
        logging.info("plug_turn_all_on")
        for plug_ip in self.plugs:
            self.plug_turn_on(plug_ip)

    def plug_turn_off(self, plug_ip):
        """Dont care."""
        logging.info("plug_turn_off " + plug_ip)
        retry = self.retries
        while retry > 0:
            retry = retry - 1
            try:
                p100 = PyP100.P100(plug_ip, self.username, self.password)
                p100.handshake()
                p100.login()
                p100.turnOff()
                time.sleep(0.25)
            except Exception as ex:
                logging.info(sys.exc_info()[0])
                logging.info(str(ex))

            time.sleep(0.25)

        return False

    def plug_turn_on(self, plug_ip):
        """Dont care."""
        logging.info("plug_turn_on " + plug_ip)
        retry = self.retries
        while retry > 0:
            retry = retry - 1
            try:
                p100 = PyP100.P100(plug_ip, self.username, self.password)
                p100.handshake()
                p100.login()
                p100.turnOn()
                time.sleep(0.25)
            except Exception as ex:
                logging.info(sys.exc_info()[0])
                logging.info(str(ex))

            time.sleep(0.25)

        return False
