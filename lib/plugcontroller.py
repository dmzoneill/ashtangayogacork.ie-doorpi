#!/usr/bin/python3
import asyncio
from kasa import SmartPlug
import time
import os

class PlugController:

    plugs = [ "192.168.8.107", "192.168.8.108", "192.168.8.109", "192.168.8.110" ]
    retries = 3
    retry_sleep = 1
    logger = None

    commands = {'info': '{"system":{"get_sysinfo":{}}}',
                'on': '{"system":{"set_relay_state":{"state":1}}}',
                'off': '{"system":{"set_relay_state":{"state":0}}}',
                'cloudinfo': '{"cnCloud":{"get_info":{}}}',
                'wlanscan': '{"netif":{"get_scaninfo":{"refresh":0}}}',
                'time': '{"time":{"get_time":{}}}',
                'schedule': '{"schedule":{"get_rules":{}}}',
                'countdown': '{"count_down":{"get_rules":{}}}',
                'antitheft': '{"anti_theft":{"get_rules":{}}}',
                'reboot': '{"system":{"reboot":{"delay":1}}}',
                'reset': '{"system":{"reset":{"delay":1}}}',
                'energy': '{"emeter":{"get_realtime":{}}}'
                }


    def __init__(self, logger):
        self.logger = logger
        self.logger.debug('started plug controller')

    def plug_turn_all_off(self):
        if os.path.exists('/var/www/html/scratch/heating_status'):
            os.unlink('/var/www/html/scratch/heating_status')

        for plug_ip in self.plugs:
            asyncio.run(self.plug_turn_off(plug_ip))

    def plug_turn_all_on(self):
        with open('/var/www/html/scratch/heating_status', 'w') as filep:
            filep.write('on')
            
        for plug_ip in self.plugs:
            asyncio.run(self.plug_turn_on(plug_ip))

    async def plug_turn_off(self, plug_ip):
        retry = self.retries
        try:
            plug = SmartPlug(plug_ip)
            await plug.update()
            while retry > 0:
                if plug.is_on == False:
                    return True
                if plug.is_on == True:
                    await plug.turn_off()
                retry = retry - 1
                time.sleep(0.25)
        except:
            self.logger.debug(sys.exc_info()[0])
            pass
        return False

    async def plug_turn_on(self, plug_ip): 
        retry = self.retries
        try:
            plug = SmartPlug(plug_ip)
            await plug.update()
            while retry > 0:
                if plug.is_on == True:
                    return True
                if plug.is_on == False:
                    await plug.turn_on()
                retry = retry - 1
                time.sleep(0.25)
        except:
            self.logger.debug(sys.exc_info()[0])
            pass
        return False
