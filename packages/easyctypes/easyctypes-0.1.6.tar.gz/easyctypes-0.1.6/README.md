# easyctypes

A Python module using `ctypes` for advanced system-level functionality such as mouse control and device access.

## Installation

You can install this package via pip:

```bash
pip install easyctypes
```

## Usage

```python
from easyctypes import move_mouse, click_mouse, list_devices

# Move the mouse to position (200, 300)
move_mouse(200, 300)

# Simulate a left mouse click
click_mouse()

# List available devices
devices = list_devices()
print(devices)
```