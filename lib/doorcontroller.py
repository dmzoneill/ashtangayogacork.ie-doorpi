#!/usr/bin/python3
import threading
import time
import RPi.GPIO as GPIO
import time
import os
import sys
from websocket_server import WebsocketServer

class DoorController:

    logger = None

    server = None    
    wsport = 9001

    buzzer_input = 21
    door_release_output = 20
    buzzer_event_completed = True
    last_time = time.time()

    def __init__(self, logger):
        self.logger = logger
        self.logger.debug('Started door controller')
        self.gpio_setup()
        thread1 = threading.Thread(target=self.websocket_setup, args=())
        thread1.daemon = True
        thread1.start()
    
    def gpio_setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_input, GPIO.IN)
        GPIO.setup(self.door_release_output, GPIO.OUT)
        GPIO.add_event_detect(self.buzzer_input, GPIO.FALLING, callback=self.buzzer_handler) 
        self.logger.info('Door GPIO setup complete')

    def websocket_setup(self):
        self.server = WebsocketServer(self.wsport, host='0.0.0.0')
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.msg_received)
        self.logger.info('Door WebsocketServer setup complete')
        self.server.run_forever()

    def buzzer_handler(self, pin):
        self.open_door()

    def client_left(self, cl, server):
        try:
            self.logger.info("Door Client (%s) left" % cl['id'])
        except:
            self.logger.error("Door failed disconnect")

    def new_client(self, cl, server):
        try:
            self.logger.info("Door New client (%s) connected" % cl['id'])
        except:
            self.logger.error("Door failed connect")

    def msg_received(self, cl, server, msg):
        if 'refresh' in msg:
            self.logger.info(msg)
            self.server.send_message_to_all(msg)
            return
        self.logger.info("Door Client (%s) : %s" % (cl['id'], msg))
        self.open_door()

    def open_door(self):
        if self.last_time + 20 > time.time():
            self.last_time = time.time()
            return

        if os.path.isfile('/var/www/html/scratch/enabled') == False:
            GPIO.output(self.door_release_output, False)
            self.last_time = time.time()
            return

        GPIO.output(self.door_release_output, True)   
        self.server.send_message_to_all(str(True))               
        time.sleep(0.2)        
        GPIO.output(self.door_release_output, False) 
        self.server.send_message_to_all(str(False))             
