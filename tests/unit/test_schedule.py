"""Define unit test of schedule class."""
import json
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

sys.path.append(".")
sys.modules["adafruit_dht"] = MagicMock()
sys.modules["board"] = MagicMock()

from lib.schedule import Schedule  # noqa


class TestSchedule(unittest.TestCase):
    """Dont care."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixture."""
        # Load default config
        cls.logger = MagicMock()
        cls.WSManager = MagicMock()

    def setUp(self):
        """Set up test fixture."""
        self.schedule = Schedule(self.WSManager, self.logger)

    @patch("builtins.open", create=True)
    @patch("lib.schedule.json.load")
    def test_read_settings(self, mock_json, mock_open):
        """Set up test fixture."""
        self.schedule.read_settings()
        mock_open.return_value = True
        mock_json.return_value = json.dumps(
            [
                {
                    "id": "1",
                    "date": "2020-11-07",
                    "start_time": "09:00:00",
                    "end_time": "10:30:00",
                    "class_type": "19",
                    "class_instructor": "1",
                    "max_attendees": "30",
                    "sticky": "0",
                    "waitlist": "0",
                    "free": "0",
                    "heating": "0",
                    "sublet": "0",
                    "name": "Eunice",
                    "level": "1",
                    "msg_frequency": "0",
                    "msg_title": "",
                    "token_restriction": "0",
                    "lowTemperatureThreshold": "20",
                    "highTemperatureThreshold": "30",
                    "heatingMinutesBefore": "45",
                    "heatingMinutesRunFor": "40",
                    "doorArmedBeforeMins": "30",
                    "doorDisarmedAfterMins": "5",
                    "student_id": "1",
                    "email": "eunice@ashtangayoga.ie",
                    "ctname": "Counted Full Primary (online)",
                }
            ]
        )
        self.schedule.read_settings()

    @patch("lib.schedule.TempHumid.get_reading")
    def test_read_th(self, get_reading):
        """Set up test fixture."""
        get_reading.return_value = [20, 20]
        self.schedule.read_th()

    def test_is_boost_active(self):
        """Set up test fixture."""
        now = datetime.now()
        self.WSManager.get_boost_time.return_value = now
        self.assertEqual(self.schedule.is_boost_active(now), False)
        self.WSManager.get_boost_time.return_value = None
        self.assertEqual(self.schedule.is_boost_active(now), False)
        self.WSManager.get_boost_time.return_value = now + timedelta(minutes=1)
        self.assertEqual(self.schedule.is_boost_active(now), True)

    def test_get_todays_classes(self):
        """Set up test fixture."""
        now = datetime.now()
        self.schedule.schedule_json = [
            {
                "id": "1",
                "date": "2020-11-07",
                "start_time": "09:00:00",
                "end_time": "10:30:00",
                "class_type": "19",
                "class_instructor": "1",
                "max_attendees": "30",
                "sticky": "0",
                "waitlist": "0",
                "free": "0",
                "heating": "0",
                "sublet": "0",
                "name": "Eunice",
                "level": "1",
                "msg_frequency": "0",
                "msg_title": "",
                "token_restriction": "0",
                "lowTemperatureThreshold": "20",
                "highTemperatureThreshold": "30",
                "heatingMinutesBefore": "45",
                "heatingMinutesRunFor": "40",
                "doorArmedBeforeMins": "30",
                "doorDisarmedAfterMins": "5",
                "student_id": "1",
                "email": "eunice@ashtangayoga.ie",
                "ctname": "Counted Full Primary (online)",
            }
        ]
        self.assertIsInstance(self.schedule.get_todays_classes(now), list)
        self.assertEqual(len(self.schedule.get_todays_classes(now)), 0)

        self.schedule.schedule_json = [
            {
                "id": "1",
                "date": now.strftime("%Y-%m-%d"),
                "start_time": "09:00:00",
                "end_time": "10:30:00",
                "class_type": "19",
                "class_instructor": "1",
                "max_attendees": "30",
                "sticky": "0",
                "waitlist": "0",
                "free": "0",
                "heating": "0",
                "sublet": "0",
                "name": "Eunice",
                "level": "1",
                "msg_frequency": "0",
                "msg_title": "",
                "token_restriction": "0",
                "lowTemperatureThreshold": "20",
                "highTemperatureThreshold": "30",
                "heatingMinutesBefore": "45",
                "heatingMinutesRunFor": "40",
                "doorArmedBeforeMins": "30",
                "doorDisarmedAfterMins": "5",
                "student_id": "1",
                "email": "eunice@ashtangayoga.ie",
                "ctname": "Counted Full Primary (online)",
            }
        ]
        self.assertIsInstance(self.schedule.get_todays_classes(now), list)
        self.assertEqual(len(self.schedule.get_todays_classes(now)), 1)

    @patch("lib.schedule.TempHumid.get_reading")
    @patch("lib.schedule.Schedule.is_boost_active")
    def test_check_heating_schedule(self, is_boost_active, get_reading):
        """Set up test fixture."""
        now = datetime.now()
        get_reading.return_value = [20, 20]
        is_boost_active.return_value = False

        mins = 0 if now.minute - 10 < 0 else now.minute - 10
        start_time = datetime(now.year, now.month, now.day, now.hour, mins)
        end_time = datetime(now.year, now.month, now.day, now.hour + 2, 0)

        self.schedule.schedule_json = [
            {
                "id": "1",
                "date": now.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M:%S"),
                "end_time": end_time.strftime("%H:%M:%S"),
                "class_type": "19",
                "class_instructor": "1",
                "max_attendees": "30",
                "sticky": "0",
                "waitlist": "0",
                "free": "0",
                "heating": "0",
                "sublet": "0",
                "name": "Eunice",
                "level": "1",
                "msg_frequency": "0",
                "msg_title": "",
                "token_restriction": "0",
                "lowTemperatureThreshold": "20",
                "highTemperatureThreshold": "30",
                "heatingMinutesBefore": "45",
                "heatingMinutesRunFor": "400",
                "doorArmedBeforeMins": "30",
                "doorDisarmedAfterMins": "5",
                "student_id": "1",
                "email": "eunice@ashtangayoga.ie",
                "ctname": "Counted Full Primary (online)",
            }
        ]

        self.WSManager.get_boost_time.return_value = now
        self.assertEqual(self.schedule.check_heating_schedule(True), False)
        self.schedule.schedule_json[0]["heating"] = "1"
        self.assertEqual(self.schedule.check_heating_schedule(True), True)

        get_reading.return_value = [20, 31]
        self.assertEqual(self.schedule.check_heating_schedule(True), False)
        self.assertEqual(self.schedule.check_heating_schedule(False), False)

        get_reading.return_value = [20, 19]
        self.assertEqual(self.schedule.check_heating_schedule(False), True)

        is_boost_active.return_value = True
        self.assertEqual(self.schedule.check_heating_schedule(False), True)
        self.assertEqual(self.schedule.check_heating_schedule(True), True)

    @patch("lib.schedule.Path")
    def test_check_door_schedule(self, mock_path):
        """Set up test fixture."""
        now = datetime.now()
        mock_path.touch.return_value = True
        mock_path.exists.return_value = False

        mins = 0 if now.minute - 10 < 0 else now.minute - 10
        start_time = datetime(now.year, now.month, now.day, now.hour, mins)
        end_time = datetime(now.year, now.month, now.day, now.hour + 2, 0)

        self.WSManager.get_boost_time.return_value = now
        self.schedule.schedule_json = [
            {
                "id": "1",
                "date": now.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M:%S"),
                "end_time": end_time.strftime("%H:%M:%S"),
                "class_type": "19",
                "class_instructor": "1",
                "max_attendees": "30",
                "sticky": "0",
                "waitlist": "0",
                "free": "0",
                "heating": "0",
                "sublet": "0",
                "name": "Eunice",
                "level": "1",
                "msg_frequency": "0",
                "msg_title": "",
                "token_restriction": "0",
                "lowTemperatureThreshold": "20",
                "highTemperatureThreshold": "30",
                "heatingMinutesBefore": "45",
                "heatingMinutesRunFor": "40",
                "doorArmedBeforeMins": "30",
                "doorDisarmedAfterMins": "5",
                "student_id": "1",
                "email": "eunice@ashtangayoga.ie",
                "ctname": "Counted Full Primary (online)",
            }
        ]
        self.schedule.check_door_schedule()
