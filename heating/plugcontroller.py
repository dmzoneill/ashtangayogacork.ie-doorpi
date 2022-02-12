#!/usr/bin/python3
"""Dont care."""
import sys
import time
import logging
from kasa import SmartPlug


logging.basicConfig(level=logging.INFO)


class PlugController:
    """Dont care."""

    plugs = ["192.168.8.3", "192.168.8.4", "192.168.8.5", "192.168.8.6"]
    retries = 3

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

    def __init__(self):
        """Dont care."""
        logging.info("started plug controller")

    async def plug_turn_all_off(self):
        """Dont care."""
        logging.info("plug_turn_all_off")
        for plug_ip in self.plugs:
            await self.plug_turn_off(plug_ip)

    async def plug_turn_all_on(self):
        """Dont care."""
        logging.info("plug_turn_all_on")
        for plug_ip in self.plugs:
            await self.plug_turn_on(plug_ip)

    async def plug_turn_off(self, plug_ip):
        """Dont care."""
        logging.info("plug_turn_off " + plug_ip)
        retry = self.retries
        while retry > 0:
            retry = retry - 1
            try:
                plug = SmartPlug(plug_ip)
                await plug.update()            
                if plug.is_on is False:
                    return True
                if plug.is_on is True:
                    await plug.turn_off()
                
            except Exception as ex:
                logging.info(sys.exc_info()[0])
                logging.info(str(ex))

            time.sleep(0.25)

        return False

    async def plug_turn_on(self, plug_ip):
        """Dont care."""
        logging.info("plug_turn_on " + plug_ip)
        retry = self.retries
        while retry > 0:
            retry = retry - 1
            try:
                plug = SmartPlug(plug_ip)
                await plug.update()            
                if plug.is_on is True:
                    return True
                if plug.is_on is False:
                    await plug.turn_on()                
                time.sleep(0.25)
            except Exception as ex:
                logging.info(sys.exc_info()[0])
                logging.info(str(ex))

            time.sleep(0.25)

        return False
