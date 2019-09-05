import time
import RPi.GPIO as GPIO
import time
import os
from websocket_server import WebsocketServer

num = 1
sound_input = 19;
light_output = 21;
last_time = time.time();
light_state = False
server = WebsocketServer(9001, host='0.0.0.0')
sleep_time = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(sound_input, GPIO.IN)
GPIO.setup(light_output, GPIO.OUT)

def client_left(cl, server):
    global client
    msg = "Client (%s) left" % cl['id']
    print(msg)

def new_client(cl, server):
    global client
    msg = "New client (%s) connected" % cl['id']
    print(msg)

def msg_received(cl, server, msg):
    global client
    msg = "Client (%s) : %s" % (cl['id'], msg)
    print(msg)

def buttonEventHandler_rising (pin):

    if os.path.isfile('/var/www/html/enabled') == False:
        GPIO.output(light_output, False)
        return;

    global num, last_time, light_state, server, sleep_time
    if time.time() >= last_time:
        for x in range(3):
            print( str(num) + ": " + str(light_state))
            num = num + 1
            last_time = time.time() + sleep_time;

            light_state = not light_state
            GPIO.output(light_output, light_state)
            
            server.send_message_to_all(str(light_state))
            time.sleep(sleep_time)
            
            server.send_message_to_all(str(False))
            
            light_state = not light_state
            GPIO.output(light_output, light_state)
            print( str(num) + ": " + str(light_state))
            time.sleep(sleep_time)


GPIO.add_event_detect(sound_input, GPIO.RISING, callback=buttonEventHandler_rising) 

try:
    if os.path.isfile('/var/www/html/enabled'):
        os.remove('/var/www/html/enabled')

    server.set_fn_client_left(client_left)
    server.set_fn_new_client(new_client)
    server.set_fn_message_received(msg_received)
    server.run_forever()
except:
    GPIO.cleanup()      
