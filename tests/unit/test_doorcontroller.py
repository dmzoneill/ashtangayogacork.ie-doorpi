"""Define unit test of schedule class."""
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(".")

MockRPi = MagicMock()
modules = {
    "RPi": MockRPi,
    "RPi.GPIO": MockRPi.GPIO,
    "threading": MagicMock(),
    "websocket_server": MagicMock(),
}
patcher = patch.dict("sys.modules", modules)
patcher.start()

from lib.doorcontroller import DoorController  # noqa


class TestDoorController(unittest.TestCase):
    """Dont care."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixture."""
        # Load default config
        cls.logger = MagicMock()
        cls.server = MagicMock()

    def setUp(self):
        """Set up test fixture."""
        self.doorcontroller = DoorController(self.logger)

    def test_gpio_setup(self):
        """Set up test fixture."""
        self.doorcontroller.gpio_setup()

    def test_websocket_setup(self):
        """Set up test fixture."""
        self.doorcontroller.websocket_setup()

    def test_buzzer_handler(self):
        """Set up test fixture."""
        self.doorcontroller.buzzer_handler(5)

    def test_client_left(self):
        """Set up test fixture."""
        self.doorcontroller.client_left(None, None)

    def test_new_client(self):
        """Set up test fixture."""
        self.doorcontroller.new_client(None, None)

    def test_msg_received(self):
        """Set up test fixture."""
        cl = {"id": "1"}
        self.doorcontroller.msg_received(cl, None, "")

    def test_msg_received_refresh(self):
        """Set up test fixture."""
        cl = {"id": "1"}
        self.doorcontroller.server = MagicMock()
        self.doorcontroller.msg_received(cl, None, "refresh")

    def test_open_door_time_not_lapsed(self):
        """Set up test fixture."""
        self.assertEqual(self.doorcontroller.open_door(), False)

    @patch("lib.doorcontroller.isfile")
    @patch("lib.doorcontroller.Gpio.output")
    @patch("lib.doorcontroller.time.time")
    def test_open_door_time_lapsed_disabled(self, mock_time, mock_gpio, mock_isfile):
        """Set up test fixture."""
        self.doorcontroller.server = MagicMock()
        self.doorcontroller.server.send_message_to_all = MagicMock()

        mock_time.return_value = 9999999999
        mock_gpio.return_value = False
        mock_isfile.return_value = False
        self.assertEqual(self.doorcontroller.open_door(), False)

    @patch("lib.doorcontroller.isfile")
    @patch("lib.doorcontroller.Gpio.output")
    @patch("lib.doorcontroller.time.time")
    def test_open_door_time_lapsed_enabled(self, mock_time, mock_gpio, mock_isfile):
        """Set up test fixture."""
        self.doorcontroller.server = MagicMock()
        self.doorcontroller.server.send_message_to_all = MagicMock()

        mock_time.return_value = 9999999999
        mock_gpio.return_value = True
        mock_isfile.return_value = True
        self.assertEqual(self.doorcontroller.open_door(), True)
