#!/usr/bin/python

import time
import board
import adafruit_dht
import os

class TempHumid:

    sensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    logger = None
    lasttemp = 0
    lasthum = 0

    def __init__(self, logger):
        self.logger = logger
        
    def get_reading(self):
        self.logger.info('Reading: ')
        x = 0

        while x < 3:
            x = x + 1
            try:
                self.lasttemp = self.sensor.temperature
                self.lasthum = self.sensor.humidity
                with open('/var/www/html/scratch/temperature', 'w') as filep1:
                    filep1.write(str(self.lasttemp))
                with open('/var/www/html/scratch/humidity', 'w') as filep2:
                    filep2.write(str(self.lasthum))
                self.logger.info('Read Temp: ' + str(self.lasttemp) + ', Hum: ' + str(self.lasthum))
                return self.lasthum, self.lasttemp
            except RuntimeError as error:
                self.logger.info('error: ' + str(error))
                time.sleep(1.0)
                continue
            except Exception as error:
                self.logger.info('error: ' + str(error))
                time.sleep(1.0)
                continue
        return self.lasthum, self.lasttemp
