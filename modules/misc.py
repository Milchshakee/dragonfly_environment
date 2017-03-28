from dragonfly import *
import re
from mouse import stop_marking

data = {
    "go to start": Key("c-a/3, left"),
    "go to end": Key("c-a/3, right"),
    "up [<n>]": Key("up:%(n)d"),
    "down [<n>]": Key("down:%(n)d"),
    "left [<n>]": Key("left:%(n)d"),
    "right [<n>]": Key("right:%(n)d"),
    "page up [<n>]": Key("pgup:%(n)d"),
    "page down [<n>]": Key("pgdown:%(n)d"),
    "up <n> (page|pages)": Key("pgup:%(n)d"),
    "down <n> (page|pages)": Key("pgdown:%(n)d"),
    "left <n> (word|words)": Key("c-left/3:%(n)d/10"),
    "right <n> (word|words)": Key("c-right/3:%(n)d/10"),
    "home": Key("home"),
    "end": Key("end"),
    "space [<n>]": Key("space:%(n)d"),
    "enter [<n>]": Key("enter:%(n)d"),
    "tab [<n>]": Key("tab:%(n)d"),
    "application key": Key("apps/3"),
    "win key": Key("win/3"),
    "indent [<n>]": Function(stop_marking) + Key("tab:%(n)d"),
    "unindent [<n>]": Function(stop_marking) + Key("shift:down/3, tab/3:%(n)d, shift:up/3"),
    "new line [<n>]": Key("end/3, enter/3:%(n)d"),
    "new line here [<n>]": Mouse("left") + Key("end/3, enter/3:%(n)d"),


    "undo": Key("c-z/3"),
    "undo <n> [times]": Key("c-z/3:%(n)d"),
    "redo": Key("c-y/3"),
    "redo <n> [times]": Key("c-y/3:%(n)d"),

    "(hold|press) alt": Key("alt:down/3"),
    "release alt": Key("alt:up"),
    "(hold|press) shift": Key("shift:down"),
    "release shift": Key("shift:up"),
    "(hold|press) control": Key("ctrl:down/3"),
    "release control": Key("ctrl:up"),
    "angle brackets": Key("langle, rangle, left/3"),
    "brackets": Key("lbracket, rbracket, left/3"),
    "braces": Key("lbrace, rbrace, left/3"),
    "parens": Key("lparen, rparen, left/3"),
}


class KeystrokeRule(MappingRule):
    mapping = data
    extras = [
        IntegerRef("n", 1, 100)
    ]
    defaults = {
        "n": 1,
    }


def create_grammar():
    grammar = Grammar("miscellaneous")
    grammar.add_rule(KeystrokeRule())
    return grammar, True
