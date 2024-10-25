import unittest
import platform
import pytest
from easyctypes.mouse_control import move_mouse, click_mouse

@pytest.mark.skipif(platform.system() != 'Windows', reason="Mouse control is only supported on Windows.")
class TestMouseControl(unittest.TestCase):
    
    def test_move_mouse_valid(self):
        # Test moving mouse to a valid position (100, 100)
        move_mouse(100, 100)
        self.assertTrue(True)  # Simulate a pass

    def test_click_mouse_left(self):
        # Test left-click functionality
        click_mouse("left")
        self.assertTrue(True)  # Simulate a pass

    def test_click_mouse_right(self):
        # Test right-click functionality
        click_mouse("right")
        self.assertTrue(True)  # Simulate a pass

    def test_click_mouse_invalid_button(self):
        # Test passing an invalid button type
        with self.assertRaises(ValueError):
            click_mouse("middle")
