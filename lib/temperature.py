#!/usr/bin/python

import Adafruit_DHT
import os

class TempHumid:

    sensor = Adafruit_DHT.DHT22
    pin = 23
    logger = None

    def __init__(self, logger):
        self.logger = logger
        
    def get_reading(self):
        self.logger.info('Reading: ')
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        
        with open('/var/www/html/scratch/temperature', 'w') as filep1:
            filep1.write(str(temperature))

        with open('/var/www/html/scratch/humidity', 'w') as filep2:
            filep2.write(str(humidity))

        self.logger.info('Read Temp: ' + str(temperature) + ', Hum: ' + str(humidity))
        return humidity, temperature

