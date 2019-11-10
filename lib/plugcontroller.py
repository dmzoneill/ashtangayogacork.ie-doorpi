#!/usr/bin/python
import socket
import threading
import json
import time
import os
from struct import pack

class PlugController:

    plugs = [ "10.42.0.10", "10.42.0.20", "10.42.0.30", "10.42.0.40" ]
    plug_port = 9999
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
        self.logger.debug('started')

    def encrypt(self, string):
        key = 171
        result = pack('>I', len(string))
        for i in string:
            a = key ^ ord(i)
            key = a
            result += chr(a)
        return result

    def decrypt(self, string):
        key = 171
        result = ""
        for i in string:
            a = key ^ ord(i)
            key = ord(i)
            result += chr(a)
        return result

    def plug_turn_all_off(self):
        if os.path.exists('/var/www/html/scratch/heating_status'):
            os.unlink('/var/www/html/scratch/heating_status')

        for plug_ip in self.plugs:
            if self.plug_turn_off(plug_ip) == False:
                self.logger.info('Failed to turn off ' + str(plug_ip))

    def plug_turn_all_on(self):
        with open('/var/www/html/scratch/heating_status', 'w') as filep:
            filep.write('on')
            
        for plug_ip in self.plugs:
            if self.plug_turn_on(plug_ip) == False:
                self.logger.info('Failed to turn on ' + str(plug_ip))


    def plug_turn_off(self, plug_ip):
        retry = self.retries
        while retry > 0:
            state = self.plug_get_on_off_state(plug_ip)
            if str(state) == "0":
                return True
            else:
                self.plug_do_command(plug_ip, self.commands["off"])
                retry = retry - 1
        return False

    def plug_turn_on(self, plug_ip): 
        retry = self.retries
        while retry > 0:
            state = self.plug_get_on_off_state(plug_ip)
            if str(state) == "1":
                return True
            else:
                self.plug_do_command(plug_ip, self.commands["on"])
                retry = retry - 1
        return False
            
    def plug_get_on_off_state(self, plug_ip):
        result = self.plug_do_command(plug_ip, self.commands["info"])
        if result != False:
            obj = json.loads(result)
            return obj['system']['get_sysinfo']['relay_state']
        return False

    def plug_do_command(self, plug_ip, plug_cmd):
        retry = self.retries
        while retry > 0:
            try:
                self.logger.debug('plug_ip:' + plug_ip)
                self.logger.debug('plug_cmd:' + plug_cmd)
                sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock_tcp.settimeout(4)
                sock_tcp.connect((plug_ip, self.plug_port))
                sock_tcp.settimeout(None)
                data = self.encrypt(plug_cmd)
                sock_tcp.send(data)
                data = sock_tcp.recv(2048)
                sock_tcp.close()
                result = self.decrypt(data[4:])
                jr = json.loads(result)
                self.logger.debug("Received: " + json.dumps(jr, indent=2, sort_keys=True))
                return result
            except socket.error as error:
                self.logger.error('socket.error:' + str(error))
                retry = retry - 1
                self.logger.warning('retrying: ' + str(retry))

            self.logger.critical('Failed after ' + str(self.retries) + ' attempts')
        return False
