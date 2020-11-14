#!/usr/bin/python3
"""Dont care."""
import filecmp
import os
from shutil import copyfile

from lirc import Lirc


class HooverController:
    """Dont care."""

    logger = None
    lircd = None

    def __init__(self, logger):
        """Dont care."""
        self.lircd = Lirc()
        self.logger = logger
        self.logger.debug("Started hoover controller")
        ret1 = self.check_config(
            "/var/www/html/conf/lirc_options.conf", "/etc/lircd/lirc_options.conf"
        )
        ret2 = self.check_config(
            "/var/www/html/conf/lircd.conf.d/hoover.conf",
            "/etc/lircd/lircd.conf.d/hoover.conf",
        )
        if ret1 or ret2:
            self.restart_lircd()

    def check_config(self, src, dst):
        """Dont care."""
        if filecmp.cmp(src, dst):
            return False
        try:
            copyfile(src, dst)
            self.logger.debug("Updated lircd config")
            return True
        except IOError:
            return False

    def restart_lircd(self):
        """Dont care."""
        try:
            os.system("systemctl restart lircd")
            self.logger.debug("Restarted lircd")
            return True
        except Exception:
            self.logger.debug("Failed restarting lircd")
            return False

    def turn_on_hoover(self):
        """Dont care."""
        self.logger.debug("Activating hoover")
        self.lircd.send_once("clean", "hoover", 5)
        return True
