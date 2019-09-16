#!/usr/bin/python
import socket
import threading
import json
import time
import os
import pprint

from websocket_server import WebsocketServer
from struct import pack
from datetime import datetime, timedelta

import Adafruit_DHT

server = WebsocketServer(9002, host='0.0.0.0')
sensor = Adafruit_DHT.DHT22
pin = 23

heater1 = "10.42.0.10"
heater2 = "10.42.0.20"
ip1 = heater2
ip2 = heater1
port = 9999
sleep_time = 10
boost_time = None

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


def encrypt(string):
    key = 171
    result = pack('>I', len(string))
    for i in string:
        a = key ^ ord(i)
        key = a
        result += chr(a)
    return result


def decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ ord(i)
        key = ord(i)
        result += chr(a)
    return result


def client_left(cl, server):
    global client
    msg = "Client (%s) left" % cl['id']
    print(msg)


def new_client(cl, server):
    global client
    msg = "New client (%s) connected" % cl['id']
    print(msg)


def msg_received(cl, server, msg):
    global client, boost_time, ip1, ip2
    msg = "Client (%s) : %s" % (cl['id'], msg)
    if boost_time is None:
        boost_time = datetime.now() + timedelta(minutes=15)
        change_heating_state(ip1,True)
        change_heating_state(ip2,True)
    else:
        boost_time = None
        change_heating_state(ip1,False)
        change_heating_state(ip2,False)

    print(msg)


def check_schedule(schedule_json, heating_json, cstate):
    global boost_time, server

    now = datetime.now()

    if boost_time != None:
        if now < boost_time:
            return True
        else:
            boost_time = None

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    with open('/var/www/html/temperature', 'w') as filep1:
        filep1.write(str(temperature))

    with open('/var/www/html/humidity', 'w') as filep2:
        filep2.write(str(humidity))

    server.send_message_to_all(str(temperature) + "," + str(humidity))

    for classobj in schedule_json:
        nowymd = now.strftime("%Y-%m-%d")
        classymd = classobj['date']

        if nowymd != classymd:
            continue

        shour = int(classobj['start_time'][0:2])
        smin = int(classobj['start_time'][3:5])

        start_time = datetime(now.year, now.month, now.day, shour, smin) - timedelta(minutes=int(heating_json['schedule_minutes_prior']))
        end_time = start_time + timedelta(minutes=int(heating_json['schedule_run_period']))

        if now > start_time and now < end_time:
            if int(temperature) <= int(heating_json['schedule_on_temp']):
                return True
            elif cstate and int(temperature) <= int(heating_json['schedule_cutoff_temp']):
                return True
            else:
                return False

    return False


def change_heating_state(host, state):
    global port
    cmd = commands["on" if state else "off"]
 
    try:
        print(cmd)
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((host, port))
        sock_tcp.send(encrypt(cmd))
        data = sock_tcp.recv(2048)
        sock_tcp.close()
        print("Sent:     " + cmd)
        print("Received: " + decrypt(data[4:]))
    except socket.error:
        pass


def main_loop(bool1, bool2):

    global server, sleep_time, ip1, ip2
    heating_state = False

    while True:

        heating_json = None
        schedule_json = None

        try:
            myfile1 = open('/var/www/html/heating.json', "r+")
            heating_json = json.load(myfile1)

            myfile2 = open('/var/www/html/schedule.json', "r+")
            schedule_json = json.load(myfile2)
        except IOError:
            time.sleep(sleep_time)
            continue

        pprint.pprint(heating_json)

        if heating_json['schedule_toggle'] == "false":
            time.sleep(sleep_time)
            continue

        new_heating_state = check_schedule(schedule_json, heating_json, heating_state)

        if new_heating_state != heating_state:
            print("state change to: " + str(new_heating_state))
            heating_state = new_heating_state
            change_heating_state(ip1,new_heating_state)
            change_heating_state(ip2, new_heating_state)
            server.send_message_to_all(str(new_heating_state))

            if new_heating_state == True:
                with open('/var/www/html/heating_status', 'w') as filep:
                    filep.write('on')
            else:
                os.unlink('/var/www/html/heating_status')
        else:
            print("state same:" + str(new_heating_state))

        time.sleep(sleep_time)


try:
    thread1 = threading.Thread(target=main_loop, args=(False, False))
    thread1.start()

    server.set_fn_client_left(client_left)
    server.set_fn_new_client(new_client)
    server.set_fn_message_received(msg_received)
    server.run_forever()
except:
    pass
