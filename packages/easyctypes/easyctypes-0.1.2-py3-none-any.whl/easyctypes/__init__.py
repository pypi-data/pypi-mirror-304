"""
easyctypes: A simple Python module for ctypes-based mouse and device control.
"""

# Importing functions from the mouse_control module
from .mouse_control import move_mouse, click_mouse, scroll_mouse

# Importing functions from the devices module
from .devices import list_devices, access_device

# Expose the functions at the package level
__all__ = [
    'move_mouse',
    'click_mouse',
    'scroll_mouse',
    'list_devices',
    'access_device'
]
