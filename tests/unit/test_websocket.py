"""Define unit test of schedule class."""
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(".")

modules = {"websocket_server": MagicMock()}
patcher = patch.dict("sys.modules", modules)
patcher.start()

from lib.websocket import WSManager  # noqa


class TestWSManager(unittest.TestCase):
    """Dont care."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixture."""
        # Load default config
        cls.logger = MagicMock()
        cls.plug_controller = MagicMock()

    def setUp(self):
        """Set up test fixture."""
        self.wsmanager = WSManager(self.plug_controller, self.logger)

    def test_client_left(self):
        """Set up test fixture."""
        self.wsmanager.client_left(MagicMock(), MagicMock())

    def test_new_client(self):
        """Set up test fixture."""
        self.wsmanager.new_client(MagicMock(), MagicMock())

    def test_msg_received(self):
        """Set up test fixture."""
        self.wsmanager.msg_received(MagicMock(), MagicMock(), MagicMock())

    def test_msg_received_boost_time_not_none(self):
        """Set up test fixture."""
        self.wsmanager.boost_time = True
        self.wsmanager.msg_received(MagicMock(), MagicMock(), MagicMock())

    def test_send(self):
        """Set up test fixture."""
        self.wsmanager.send(MagicMock())

    def test_send_exception(self):
        """Set up test fixture."""
        debug = MagicMock()
        debug.side_effect = Exception
        self.logger.debug = debug
        # self.logger.debug.side_effect = Exception
        try:
            self.wsmanager.send(MagicMock())
        except Exception:
            self.logger.debug = MagicMock()

    def test_get_boost_time(self):
        """Set up test fixture."""
        self.wsmanager.get_boost_time()

    def test_set_boost_time(self):
        """Set up test fixture."""
        self.wsmanager.set_boost_time(True)

    def test_run(self):
        """Set up test fixture."""
        self.wsmanager.run()
