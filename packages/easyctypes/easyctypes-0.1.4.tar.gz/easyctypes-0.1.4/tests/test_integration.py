import unittest
import platform
from easyctypes.mouse_control import move_mouse, click_mouse
from easyctypes.devices import access_device, list_devices

class TestIntegration(unittest.TestCase):

    @unittest.skipIf(platform.system() != 'Windows', "Integration test only valid on Windows")
    def test_mouse_and_device_integration(self):
        # Move mouse and then access a device
        move_mouse(100, 100)
        devices = access_device(list_devices()[0])
        self.assertTrue(devices)
        click_mouse("left")
