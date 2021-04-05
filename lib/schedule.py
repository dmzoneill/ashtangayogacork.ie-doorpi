#!/usr/bin/python
"""Dont care."""
import json
from datetime import datetime, timedelta
from pathlib import Path
import time

from lib.temperature import TempHumid


class Schedule:
    """Dont care."""

    logger = None
    schedule_json = None
    wsmnager = None

    def __init__(self, wsmnager, logger):
        """Dont care."""
        self.logger = logger
        self.wsmnager = wsmnager
        self.logger.debug("schedule started")

    def read_settings(self):
        """Dont care."""
        try:
            myfile2 = open("/var/www/html/scratch/schedule.json", "r+")
            self.schedule_json = json.load(myfile2)
            self.logger.info(json.dumps(self.schedule_json, indent=4, sort_keys=True))
        except TypeError:
            self.logger.error("Error reading schedule/heating config")
        except IOError:
            self.logger.error("Error reading schedule/heating config")

    def read_th(self):
        """Dont care."""
        th = TempHumid(self.logger)
        humidity, temperature = th.get_reading()
        self.wsmnager.send(str(temperature) + "," + str(humidity))
        self.logger.debug(str(temperature) + "," + str(humidity))
        return humidity, temperature

    def is_boost_active(self, now):
        """Dont care."""
        if self.wsmnager.get_boost_time() is not None:
            if now < self.wsmnager.get_boost_time():
                self.logger.debug("Heating Boost active")
                return True
            else:
                self.wsmnager.set_boost_time(None)
                return False
        return False

    def get_todays_classes(self, now):
        """Dont care."""
        todays = []
        for classobj in self.schedule_json:
            nowymd = now.strftime("%Y-%m-%d")
            classymd = classobj["date"]

            if nowymd != classymd:
                continue

            todays.append(classobj)

        return todays

    def check_heating_schedule(self, current_state):
        """Dont care."""
        now = datetime.now()
        humidity, temperature = self.read_th()
        boost_active = self.is_boost_active(now)

        while humidity is None:
            self.logger.debug("Sensor data was null")
            time.sleep(10)
            humidity, temperature = self.read_th()

        self.logger.debug("humidity: " + str(humidity))
        self.logger.debug("temperature: " + str(temperature))

        if boost_active is True:
            return True

        for classobj in self.get_todays_classes(now):

            shour = int(classobj["start_time"][0:2])
            smin = int(classobj["start_time"][3:5])

            start_time = datetime(
                now.year, now.month, now.day, shour, smin
            ) - timedelta(minutes=int(classobj["heatingMinutesBefore"]))
            end_time = start_time + timedelta(
                minutes=int(classobj["heatingMinutesRunFor"])
            )

            self.logger.debug("Heating Now: " + str(now))
            self.logger.debug("Heating Start_time: " + str(start_time))
            self.logger.debug("Heating End_time: " + str(end_time))
            self.logger.debug("Heating state for class: " + str(classobj["heating"]))

            if now > start_time and now < end_time:
                self.logger.debug("Within schedule time delta")
                if int(classobj["heating"]) == 0:
                    self.logger.debug("Heating disabled for class")
                    return False
                if current_state is True:
                    if int(temperature) <= int(classobj["highTemperatureThreshold"]):
                        self.logger.debug(
                            "Continue heating: less than <"
                            + str(classobj["highTemperatureThreshold"])
                        )
                        return True
                    else:
                        self.logger.debug(
                            "End heating: greater than >"
                            + str(classobj["highTemperatureThreshold"])
                        )
                        return False
                else:
                    if int(temperature) <= int(classobj["lowTemperatureThreshold"]):
                        self.logger.debug(
                            "Start heating: less than <"
                            + str(classobj["lowTemperatureThreshold"])
                        )
                        return True

        self.logger.debug("No heating today/now: False")
        return False

    def check_door_schedule(self):
        """Dont care."""
        path = "/var/www/html/scratch/enabled"
        now = datetime.now()

        for classobj in self.get_todays_classes(now):

            shour = int(classobj["start_time"][0:2])
            smin = int(classobj["start_time"][3:5])

            start_time = datetime(
                now.year, now.month, now.day, shour, smin
            ) - timedelta(minutes=int(classobj["doorArmedBeforeMins"]))
            end_time = datetime(now.year, now.month, now.day, shour, smin) + timedelta(
                minutes=int(classobj["doorDisarmedAfterMins"])
            )

            self.logger.debug("Door Now: " + str(now))
            self.logger.debug("Door Start_time: " + str(start_time))
            self.logger.debug("Door End_time: " + str(end_time))

            if now > start_time and now < end_time:
                if Path(path).exists() is False:
                    Path(path).touch()
                self.logger.debug("Door Within schedule time delta")
                return

        self.logger.debug("Door disabled now")
        if Path(path).exists():
            Path(path).unlink()

    def check_hoover_schedule(self):
        """Dont care."""
        now = datetime.now()

        for classobj in self.get_todays_classes(now):

            shour = int(classobj["start_time"][0:2])
            smin = int(classobj["start_time"][3:5])

            start_time = datetime(
                now.year, now.month, now.day, shour, smin
            ) - timedelta(minutes=150)
            end_time = datetime(now.year, now.month, now.day, shour, smin) - timedelta(
                minutes=148
            )

            self.logger.debug("Hoover Now: " + str(now))
            self.logger.debug("Hoover Start_time: " + str(start_time))

            if now > start_time and now < end_time:
                self.logger.debug("Hoover should start now")
                return True

        self.logger.debug("Dont start hoover")
        return False
