import platform
import ctypes
import os

# This function lists available devices depending on the operating system
def list_devices():
    """
    Returns a list of available devices based on the platform.
    On Windows, it lists HID devices (like keyboards, mice, etc.).
    On Linux/Mac, it lists connected input devices.
    """
    system = platform.system()

    if system == 'Windows':
        # Windows-specific: use ctypes to access Windows API for device listing
        devices = _list_windows_devices()
    elif system == 'Linux':
        # Linux-specific: parse /dev/input for connected input devices
        devices = _list_linux_devices()
    elif system == 'Darwin':
        # macOS-specific: currently stubbed out
        devices = _list_macos_devices()
    else:
        raise OSError(f"Unsupported platform: {system}")

    return devices

def access_device(device_name):
    """
    Simulates accessing a device by name.
    Returns True if the device is successfully accessed, raises an error otherwise.
    """
    if device_name in list_devices():
        # Simulate device access, this can be customized to actual device control
        return True
    else:
        raise OSError(f"Device '{device_name}' not found.")


def _list_windows_devices():
    """
    Private function to list Windows HID devices using ctypes.
    """
    # For demonstration purposes, we return a mock list.
    # You can extend this to use ctypes to call Windows API functions for device listing.
    return ["HID-compliant mouse", "HID-compliant keyboard", "USB Camera"]

def _list_linux_devices():
    """
    Private function to list Linux input devices by scanning /dev/input.
    """
    input_dir = '/dev/input'
    if os.path.exists(input_dir):
        return os.listdir(input_dir)
    else:
        return []

def _list_macos_devices():
    """
    Private function to list macOS input devices.
    """
    # Stub for macOS device listing
    return ["Apple Keyboard", "Apple Magic Mouse"]
