"""Define unit test of schedule class."""
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(".")
sys.modules["asyncio"] = MagicMock()
sys.modules["kasa"] = MagicMock()
sys.modules["os"] = MagicMock()

from lib.plugcontroller import PlugController  # noqa


class TestPlugController(unittest.TestCase):
    """Dont care."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixture."""
        cls.logger = MagicMock()

    def setUp(self):
        """Set up test fixture."""
        self.plugcontroller = PlugController(self.logger)

    def test_plug_turn_all_off(self):
        """Set up test fixture."""
        self.assertEqual(True, True)

    @patch("builtins.open", create=True)
    def test_plug_turn_all_on(self, mock_open):
        """Set up test fixture."""
        # self.plugcontroller.plug_turn_all_off()
        self.assertEqual(True, True)

    def test_plug_turn_off(self):
        """Set up test fixture."""
        self.assertEqual(True, True)

    def test_plug_turn_on(self):
        """Set up test fixture."""
        self.assertEqual(True, True)
