from dragonfly import *


data = {
    "go to top": Key("c-home"),
    "go to bottom": Key("c-end"),
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
    "start of line": Key("home"),
    "end of line": Key("end"),
    "application key": Key("apps/3"),
    "win key": Key("win/3"),

    "(hold|press) alt": Key("alt:down/3"),
    "release alt": Key("alt:up"),
    "(hold|press) shift": Key("shift:down"),
    "release shift": Key("shift:up"),
    "(hold|press) control": Key("ctrl:down/3"),
    "release control": Key("ctrl:up"),

    "enter": Key("enter/3"),

    "stop listening": Key("ca-m")
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
