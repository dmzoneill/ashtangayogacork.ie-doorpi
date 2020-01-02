#!/usr/bin/python
import json

from datetime import datetime, timedelta
from lib.temperature import TempHumid

class Schedule:

    logger = None
    heating_json = None
    schedule_json = None
    wsmnager = None

    def __init__(self, WSManager, logger):
        self.logger = logger
        self.wsmnager = WSManager
        self.logger.debug('started')
    
    def read_settings(self):
        try:
            myfile1 = open('/var/www/html/scratch/heating.json', "r+")
            self.heating_json = json.load(myfile1)
            self.logger.info(json.dumps(self.heating_json, indent=4, sort_keys=True))

            myfile2 = open('/var/www/html/scratch/schedule.json', "r+")
            self.schedule_json = json.load(myfile2)
            self.logger.info(json.dumps(self.schedule_json, indent=4, sort_keys=True))
        except IOError:
            self.logger.error("Error reading schedule/heating config")

    def read_th(self):
        th = TempHumid(self.logger)
        humidity, temperature = th.get_reading()
        self.wsmnager.send(str(temperature) + "," + str(humidity))
        self.logger.debug(str(temperature) + "," + str(humidity))
        return humidity, temperature

    def is_boost_active(self, now):
        if self.wsmnager.get_boost_time() != None:
            if now < self.wsmnager.get_boost_time():
                self.logger.debug('Boost active')
                return True
            else:
                self.wsmnager.set_boost_time(None)
                return False
        return False

    def get_todays_classes(self, now):
        todays = []
        for classobj in self.schedule_json:
            nowymd = now.strftime("%Y-%m-%d")
            classymd = classobj['date']

            if nowymd != classymd:
                continue

            todays.append(classobj)

        return todays

    def check_schedule(self, current_state):
        self.read_settings()

        now = datetime.now()
        humidity, temperature = self.read_th()
        boost_active = self.is_boost_active(now)

        if boost_active == True:
            return True

        if self.heating_json['schedule_toggle'] == "false":
            self.logger.debug('schedule disabled')
            return False

        for classobj in self.get_todays_classes(now):

            shour = int(classobj['start_time'][0:2])
            smin = int(classobj['start_time'][3:5])

            #if classobj['heating']== "0":
            #    continue

            start_time = datetime(now.year, now.month, now.day, shour, smin) - timedelta(minutes=int(self.heating_json['schedule_minutes_prior']))
            end_time = start_time + timedelta(minutes=int(self.heating_json['schedule_run_period']))

            self.logger.debug("Now: " + str(now))
            self.logger.debug("Start_time: " + str(start_time))
            self.logger.debug("End_time: " + str(end_time))

            if now > start_time and now < end_time:
                self.logger.debug("Within schedule time delta")
                if current_state == True:
                    if int(temperature) <= int(self.heating_json['schedule_cutoff_temp']):
                        self.logger.debug("Continue heating: less than <" + str(self.heating_json['schedule_cutoff_temp']))
                        return True
                    else:
                        self.logger.debug("End heating: greater than >" + str(self.heating_json['schedule_cutoff_temp']))
                        return False
                else:
                    if int(temperature) <= int(self.heating_json['schedule_on_temp']):
                        self.logger.debug("Start heating: less than <" + str(self.heating_json['schedule_on_temp']))
                        return True

        self.logger.debug("No heating today/now: False")
        return False
