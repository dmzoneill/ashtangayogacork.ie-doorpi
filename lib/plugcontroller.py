#!/usr/bin/python3
"""Dont care."""
import asyncio
import os
import sys
import time

from kasa import SmartPlug


class PlugController:
    """Dont care."""

    plugs = ["192.168.8.107", "192.168.8.108", "192.168.8.109", "192.168.8.110"]
    retries = 3
    retry_sleep = 1
    logger = None

    commands = {
        "info": '{"system":{"get_sysinfo":{}}}',
        "on": '{"system":{"set_relay_state":{"state":1}}}',
        "off": '{"system":{"set_relay_state":{"state":0}}}',
        "cloudinfo": '{"cnCloud":{"get_info":{}}}',
        "wlanscan": '{"netif":{"get_scaninfo":{"refresh":0}}}',
        "time": '{"time":{"get_time":{}}}',
        "schedule": '{"schedule":{"get_rules":{}}}',
        "countdown": '{"count_down":{"get_rules":{}}}',
        "antitheft": '{"anti_theft":{"get_rules":{}}}',
        "reboot": '{"system":{"reboot":{"delay":1}}}',
        "reset": '{"system":{"reset":{"delay":1}}}',
        "energy": '{"emeter":{"get_realtime":{}}}',
    }

    def __init__(self, logger):
        """Dont care."""
        self.logger = logger
        self.logger.debug("started plug controller")

    def plug_turn_all_off(self):
        """Dont care."""
        if os.path.exists("/var/www/html/scratch/heating_status"):
            os.unlink("/var/www/html/scratch/heating_status")

        for plug_ip in self.plugs:
            asyncio.run(self.plug_turn_off(plug_ip))

    def plug_turn_all_on(self):
        """Dont care."""
        with open("/var/www/html/scratch/heating_status", "w") as filep:
            filep.write("on")

        for plug_ip in self.plugs:
            asyncio.run(self.plug_turn_on(plug_ip))

    async def plug_turn_off(self, plug_ip):
        """Dont care."""
        retry = self.retries
        try:
            plug = SmartPlug(plug_ip)
            await plug.update()
            while retry > 0:
                if plug.is_on is False:
                    return True
                if plug.is_on is True:
                    await plug.turn_off()
                retry = retry - 1
                time.sleep(0.25)
        except Exception as ex:
            self.logger.debug(sys.exc_info()[0])
            self.logger.debug(str(ex))
            pass
        return False

    async def plug_turn_on(self, plug_ip):
        """Dont care."""
        retry = self.retries
        try:
            plug = SmartPlug(plug_ip)
            await plug.update()
            while retry > 0:
                if plug.is_on is True:
                    return True
                if plug.is_on is False:
                    await plug.turn_on()
                retry = retry - 1
                time.sleep(0.25)
        except Exception as ex:
            self.logger.debug(sys.exc_info()[0])
            self.logger.debug(str(ex))
            pass
        return False
