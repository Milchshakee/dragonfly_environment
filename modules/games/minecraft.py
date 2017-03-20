from dragonfly import *

import win32api, win32con


def toggle_dig():
    x, y = win32api.GetCursorPos()
    if not toggle_dig.is_digging:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    else:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    toggle_dig.is_digging = not toggle_dig.is_digging;

toggle_dig.is_digging = False


def toggle_sneak():
    if not toggle_sneak.is_sneaking:
        Key("shift:down/3").execute()
    else:
        Key("shift:up/3").execute()
    toggle_sneak.is_sneaking = not toggle_sneak.is_sneaking;

toggle_sneak.is_sneaking = False

mapping = {
    "jump": Key("space:down/3, space:up/3"),
    "bip": Mouse("left"),
    "bop": Mouse("right"),
    "dig": Function(toggle_dig),
    "sneak": Function(toggle_sneak),
    "hover": Key("space:down/3, m:down/3, space:up/3, m:up/3"),
    "boost": Key("space:down/3"),
    "stop": Key("space:up/3, shift:up/3"),
    "sink": Key("shift:down/3"),
    "fly": Key("space:down/3, space:up/3, space:down/3, space:up/3"),
    "drop": Key("q"),
    "run": Key("r:down/3, r:up/3")
}


class CommandRule(MappingRule):
    mapping = mapping


def create_grammar():
    mc_context = AppContext(title="Minecraft 1.10.2")
    grammar = Grammar("minecraft", context=mc_context)
    grammar.add_rule(CommandRule())
    return grammar, True
