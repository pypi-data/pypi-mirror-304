# easyctypes/mouse_control.py

import ctypes

user32 = ctypes.windll.user32

def move_mouse(x, y):
    """
    Moves the mouse to a specific position on the screen (x, y).
    """
    user32.SetCursorPos(x, y)

def click_mouse(button="left"):
    """
    Simulates a mouse click (left or right).
    """
    if button == "left":
        user32.mouse_event(0x0002, 0, 0, 0, 0)  # Mouse left down
        user32.mouse_event(0x0004, 0, 0, 0, 0)  # Mouse left up
    elif button == "right":
        user32.mouse_event(0x0008, 0, 0, 0, 0)  # Mouse right down
        user32.mouse_event(0x0010, 0, 0, 0, 0)  # Mouse right up
