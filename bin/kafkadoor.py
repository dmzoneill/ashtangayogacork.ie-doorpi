#!/usr/bin/python3
import traceback
import time
import os
from kafka import KafkaConsumer
import subprocess

consumer = KafkaConsumer('door', bootstrap_servers=['46.101.231.44:9092'])

while True:
    try:        
        for message in consumer:
            if os.path.exists("/var/www/html/scratch/enabled"):
                print("open door")
                subprocess.run(["/var/www/html/bin/opendoor"])
            print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))

        time.sleep(1)
        print(".")
    except:
        traceback.print_exc()
        time.sleep(1)
        consumer = KafkaConsumer('door', bootstrap_servers=['46.101.231.44:9092'])

