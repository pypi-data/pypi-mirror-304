import unittest
from easyctypes.mouse_control import move_mouse

class TestErrorHandling(unittest.TestCase):

    def test_move_mouse_invalid_position(self):
        # Test moving the mouse to invalid positions
        with self.assertRaises(ValueError):
            move_mouse(-1, -1)

        with self.assertRaises(ValueError):
            move_mouse(999999, 999999)
