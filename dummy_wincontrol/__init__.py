blocked: bool = False

def is_blocked():
    global blocked
    return blocked

def enable():
    global blocked
    blocked=False
    print("enabled")

def disable():
    global blocked
    blocked=True
    print("disabled")
