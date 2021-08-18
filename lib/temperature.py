#!/usr/bin/python
"""Dont care."""
import time

import adafruit_dht

import board


class TempHumid:
    """Dont care."""

    sensor = None
    logger = None
    lasttemp = 0
    lasthum = 0

    def __init__(self, logger):
        """Dont care."""
        self.sensor = adafruit_dht.DHT22(board.D19, use_pulseio=False)
        self.logger = logger

    def get_reading(self):
        """Dont care."""
        self.logger.info("Temperature Reading: ")
        x = 0

        while x < 3:
            x = x + 1
            try:
                ltemp = self.sensor.temperature
                lhum = self.sensor.humidity
                if ltemp is not None:
                    self.lasttemp = ltemp
                    with open("/var/www/html/scratch/temperature", "w") as filep1:
                        filep1.write(str(self.lasttemp))
                if lhum is not None:
                    self.lasthum = lhum
                    with open("/var/www/html/scratch/humidity", "w") as filep2:
                        filep2.write(str(self.lasthum))
                self.logger.info(
                    "Read Temp: " + str(self.lasttemp) + ", Hum: " + str(self.lasthum)
                )
                if ltemp is not None or lhum is not None:
                    return self.lasthum, self.lasttemp
            except RuntimeError as error:
                self.logger.info("error: " + str(error))
                time.sleep(1.0)
                continue
            except Exception as error:
                self.logger.info("error: " + str(error))
                time.sleep(1.0)
                continue
        return self.lasthum, self.lasttemp
