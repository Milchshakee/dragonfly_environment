import win32api, win32con
import dragonfly.timer
from dragonfly import *


scroll_position = None
scrolling = False
marking = False


def start_marking():
    global marking
    marking = True
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    Key("shift:down").execute()


def stop_marking():
    global marking
    if marking:
        marking = False
        Key("shift:up").execute()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def toggle_marking():
    global marking
    if marking:
        stop_marking()
    else:
        start_marking()

SCROLL_THRESHOLD = 3
SCROLL_SPEED = 0.003


def get_scroll_amount(moved):
    if -SCROLL_THRESHOLD < moved < SCROLL_THRESHOLD:
        return 0
    if moved > 0:
        value = moved - SCROLL_THRESHOLD
        return int(SCROLL_SPEED * (value * value))
    else:
        value = moved + SCROLL_THRESHOLD
        return int(-SCROLL_SPEED * (value * value))


def call():
    global scrolling
    if scrolling:
        x, y = win32api.GetCursorPos()
        dx = x - scroll_position[0]
        dy = y - scroll_position[1]
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, get_scroll_amount(-dy))


def toggle_scroll():
    global scrolling
    global scroll_position
    scrolling = not scrolling
    scroll_position = win32api.GetCursorPos()


class MouseRule(MappingRule):
    mapping = {
        "scroll": Function(toggle_scroll),
        "mark": Function(toggle_marking),
        "(left-click|click)": Mouse("left"),
        "double-click": Mouse("left/3, left/3"),
        "right-click": Mouse("right")
    }


def create_grammar():
    grammar = Grammar("mouse")
    grammar.add_rule(MouseRule())
    return grammar, True


def load():
    dragonfly.timer.timer.add_callback(call, 0.01)


def unload():
    dragonfly.timer.timer.remove_callback(call)

