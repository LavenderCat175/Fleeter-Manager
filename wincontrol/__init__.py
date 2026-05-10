from wincontrol.blocker import enable_input, disable_input
from wincontrol.screen_manager import block_screen, remove_screen_block

blocked: bool = False

def is_blocked():
    global blocked
    return blocked

def enable():
    global blocked
    blocked = False
    enable_input()
    remove_screen_block()

def disable():
    global blocked
    blocked = True
    disable_input()
    block_screen()