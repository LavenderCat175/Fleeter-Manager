import pynput

mouse_blocker = pynput.mouse.Listener(suppress=True)
keyboard_blocker = pynput.keyboard.Listener(suppress=True)

def disable_input():
    global mouse_blocker, keyboard_blocker

    mouse_blocker = pynput.mouse.Listener(suppress=True)
    keyboard_blocker = pynput.keyboard.Listener(suppress=True)

    mouse_blocker.start()
    keyboard_blocker.start()

def enable_input():
    global mouse_blocker, keyboard_blocker
    mouse_blocker.stop()
    keyboard_blocker.stop()