"""Define unit test of schedule class."""
import unittest
from unittest.mock import MagicMock, patch

from lib.hoovercontroller import HooverController  # noqa


class TestHooverController(unittest.TestCase):
    """Dont care."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixture."""
        # Load default config
        cls.logger = MagicMock()

    @patch("lib.hoovercontroller.lirc")
    @patch("lib.hoovercontroller.filecmp.cmp")
    @patch("lib.hoovercontroller.os.system")
    @patch("lib.hoovercontroller.copyfile")
    def setUp(self, mock_copyfile, mock_system, mock_cmp, mock_lirc):
        """Set up test fixture."""
        mock_cmp.return_value = False
        mock_copyfile.return_value = True
        self.hoovercontroller = HooverController(self.logger)
        self.hoovercontroller.lircd = MagicMock()

    @patch("lib.hoovercontroller.filecmp.cmp")
    def test_check_config_same(self, mock_cmp):
        """Set up test fixture."""
        mock_cmp.return_value = True
        self.assertEqual(self.hoovercontroller.check_config("a", "b"), False)

    @patch("lib.hoovercontroller.copyfile")
    @patch("lib.hoovercontroller.filecmp.cmp")
    def test_check_config_not_same(self, mock_cmp, mock_copyfile):
        """Set up test fixture."""
        mock_cmp.return_value = False
        mock_copyfile.return_value = True
        self.assertEqual(self.hoovercontroller.check_config("a", "b"), True)

    @patch("lib.hoovercontroller.copyfile")
    @patch("lib.hoovercontroller.filecmp.cmp")
    def test_check_config_not_same_error(self, mock_cmp, mock_copyfile):
        """Set up test fixture."""
        mock_cmp.return_value = False
        mock_copyfile.side_effect = IOError
        self.assertEqual(self.hoovercontroller.check_config("a", "b"), False)

    @patch("lib.hoovercontroller.os.system")
    def test_restart_lircd(self, mock_system):
        """Set up test fixture."""
        mock_system.return_value = True
        self.assertEqual(self.hoovercontroller.restart_lircd(), True)
        mock_system.assert_called_once_with("systemctl restart lircd")

    @patch("lib.hoovercontroller.os.system")
    def test_restart_lircd_error(self, mock_system):
        """Set up test fixture."""
        mock_system.side_effect = Exception("Boom!")
        self.assertEqual(self.hoovercontroller.restart_lircd(), False)
        mock_system.assert_called_once_with("systemctl restart lircd")

    def test_turn_on_hoover(self):
        """Set up test fixture."""
        self.assertEqual(self.hoovercontroller.turn_on_hoover(), True)
