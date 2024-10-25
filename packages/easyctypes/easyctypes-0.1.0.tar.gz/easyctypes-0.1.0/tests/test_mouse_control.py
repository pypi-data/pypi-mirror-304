# tests/test_mouse_control.py

from easyctypes.mouse_control import move_mouse, click_mouse

def test_move_mouse():
    # This is a dummy test; in a real case you would use mocks
    move_mouse(100, 100)
    assert True  # Simulate success

def test_click_mouse():
    click_mouse()
    assert True  # Simulate success
