import unittest
import platform
import pytest
from easyctypes.devices import access_device, list_devices

class TestDeviceAccess(unittest.TestCase):

    def test_list_devices(self):
        # Test if listing devices returns a non-empty list
        devices = list_devices()
        self.assertIsInstance(devices, list)
        self.assertGreater(len(devices), 0)

    def test_access_device_valid(self):
        # Test accessing a known valid device
        device = list_devices()[0]
        self.assertTrue(access_device(device))

    def test_access_device_invalid(self):
        # Test accessing a device that doesn’t exist
        with self.assertRaises(OSError):
            access_device("invalid_device")
