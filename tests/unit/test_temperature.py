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

    @patch("builtins.open", create=True)
    @patch("lib.temperature.time.sleep")
    def test_get_reading(self, time, mock_open):
        """Set up test fixture."""
        self.temphumid.get_reading()

    @patch("builtins.open", create=True)
    @patch("lib.temperature.time.sleep")
    def test_get_reading_runtime_error(self, time, mock_open):
        """Set up test fixture."""
        mock_open.side_effect = RuntimeError
        self.temphumid.get_reading()

    @patch("builtins.open", create=True)
    @patch("lib.temperature.time.sleep")
    def test_get_reading_exception(self, time, mock_open):
        """Set up test fixture."""
        mock_open.side_effect = Exception
        self.temphumid.get_reading()
