import time
import win32api, win32con, win32gui
from dragonfly import (Grammar, Key, Mouse, DictListRef,
                       Dictation, Compound, Rule, CompoundRule,
                       DictList, Window, Rectangle, monitors,
                       Config, Section, Function, MappingRule)

import dragonfly.timer

grammar = Grammar("mouse control")
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


dragonfly.timer.timer.add_callback(call, 0.01)


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
        "(double-click|select)": Mouse("left:down, left:up, left:down, left:up"),
        "(select line)": Mouse("left:down, left:up, left:down, left:up, left:down, left:up"),
        "(right-click)": Mouse("right")
    }

grammar.add_rule(MouseRule())
grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
        dragonfly.timer.timer.remove_callback(call)
    grammar = None
