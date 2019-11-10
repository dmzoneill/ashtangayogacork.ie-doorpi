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
heater3 = "10.42.0.30"
heater4 = "10.42.0.40"
ip1 = heater1
ip2 = heater2
ip3 = heater3
ip4 = heater4
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
    global client, boost_time, ip1, ip2, ip3, ip4
    msg = "Client (%s) : %s" % (cl['id'], msg)
    if boost_time is None:
        boost_time = datetime.now() + timedelta(minutes=15)
        change_heating_state(ip1,True)
        change_heating_state(ip2,True)
        change_heating_state(ip3,True)
        change_heating_state(ip4,True)
    else:
        boost_time = None
        change_heating_state(ip1,False)
        change_heating_state(ip2,False)
        change_heating_state(ip3,False)
        change_heating_state(ip4,False)

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
    print("Temperature: " + str(temperature))
    print("Humidity: " + str(humidity))

    with open('/var/www/html/scratch/temperature', 'w') as filep1:
        filep1.write(str(temperature))

    with open('/var/www/html/scratch/humidity', 'w') as filep2:
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

        print("Now: " + str(now))
        print("Start_time: " + str(start_time))
        print("End_time: " + str(end_time))

        if now > start_time and now < end_time:
            print("Within schedule time delta")
            if int(temperature) <= int(heating_json['schedule_on_temp']):
                print("Start heating: less than <" + str(heating_json['schedule_on_temp']))
                return True
            elif cstate and int(temperature) <= int(heating_json['schedule_cutoff_temp']):
                print("Continue heating: less than <" + str(heating_json['schedule_cutoff_temp']))
                return True
            else:
                print("End heating: greater than >" + str(heating_json['schedule_cutoff_temp']))
                return False

    print("No heating today/now: False")
    return False


def change_heating_state(host, state):
    global port
    cmd = commands["on" if state else "off"]
 
    try:
        print(cmd)
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.settimeout(4)
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

    line = "========================================================"

    while True:

        print(line)
        heating_json = None
        schedule_json = None

        try:
            myfile1 = open('/var/www/html/scratch/heating.json', "r+")
            heating_json = json.load(myfile1)

            myfile2 = open('/var/www/html/scratch/schedule.json', "r+")
            schedule_json = json.load(myfile2)
        except IOError:
            time.sleep(sleep_time)
            print("Error reading schedule/heating config")
            continue

        pprint.pprint(heating_json)

        if heating_json['schedule_toggle'] == "false":
            time.sleep(sleep_time)
            continue

        heating_state = check_schedule(schedule_json, heating_json, heating_state)

        print("Set state: " + str(heating_state))
        change_heating_state(ip1,heating_state)
        change_heating_state(ip2,heating_state)
        change_heating_state(ip3,heating_state)
        change_heating_state(ip4,heating_state)
        server.send_message_to_all(str(heating_state))

        if heating_state == True:
            with open('/var/www/html/scratch/heating_status', 'w') as filep:
                filep.write('on')
        else:
            if os.path.exists('/var/www/html/scratch/heating_status'):
                os.unlink('/var/www/html/scratch/heating_status')

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
