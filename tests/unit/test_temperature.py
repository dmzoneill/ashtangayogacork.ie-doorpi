"""Define unit test of schedule class."""
import sys
import unittest
from unittest.mock import MagicMock, patch

from lib.temperature import TempHumid

sys.path.append(".")
modules = {"adafruit_dht": MagicMock(), "board": MagicMock()}
patcher = patch.dict("sys.modules", modules)
patcher.start()


class TestTemperature(unittest.TestCase):
    """Dont care."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixture."""
        # Load default config
        cls.logger = MagicMock()
        cls.sensor = MagicMock()

    def setUp(self):
        """Set up test fixture."""
        self.temphumid = TempHumid(self.logger)

    @patch("lib.temperature.time.sleep")
    def test_get_reading(self, time):
        """Set up test fixture."""
        self.sensor.temperature.side_effect = 50
        self.sensor.humidity.side_effect = 50
        self.temphumid.get_reading()
