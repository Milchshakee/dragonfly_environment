from dragonfly import *
from mouse import stop_marking


release = Key("shift:up, ctrl:up, alt:up")


def copy_command():
    # Add Command Prompt, putty, ...?
    context = AppContext(executable="console")
    window = Window.get_foreground()
    if context.matches(window.executable, window.title, window.handle):
        return
    release.execute()
    Key("c-c/3").execute()


def paste_command():
    # Add Command Prompt, putty, ...?
    context = AppContext(executable="console")
    window = Window.get_foreground()
    if context.matches(window.executable, window.title, window.handle):
        return
    release.execute()
    Key("c-v/3").execute()

actions = {
    "cut": Key("c-x/3"),
    "copy": Function(copy_command),
    "replace": Function(paste_command),
    "delete": Key("del/3")
}

scopes = {
    "all": Key("c-a/3"),
    "line": Mouse("left/3, left/3, left/3"),
    "this": Mouse("left/3, left/3"),
    "[selection]": Function(stop_marking)
}


class ActionRule(CompoundRule):
    spec = "<action> <scope>"
    extras = [
        Choice("action", actions),
        Choice("scope", scopes)
    ]

    def _process_recognition(self, node, extras):
        action = extras["action"]
        scope = extras["scope"]
        scope.execute()
        Pause("3")
        action.execute()

commands = {
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
    "space [<n>]": release + Key("space:%(n)d"),
    "enter [<n>]": release + Key("enter:%(n)d"),
    "tab [<n>]": Key("tab:%(n)d"),
    "delete <n>": Key("del/3:%(n)d"),
    "(back|backspace) [<n>]": release + Key("backspace/1:%(n)d"),
    "application key": release + Key("apps/3"),
    "win key": release + Key("win/3"),
    "paste": Function(paste_command),
    "paste here": Mouse("left") + Function(paste_command),
    "select": Mouse("left/3, left/3"),
    "select line": Mouse("left/3, left/3, left/3"),
    "select all": Key("c-a/3"),
    "indent [<n>]": Key("tab:%(n)d"),
    "unindent [<n>]": Key("shift:down/3, tab/3:%(n)d, shift:up/3"),

    "undo": release + Key("c-z/3"),
    "undo <n> [times]": release + Key("c-z/3:%(n)d"),
    "redo": release + Key("c-y/3"),
    "redo <n> [times]": release + Key("c-y/3:%(n)d"),

    "(hold|press) alt": Key("alt:down/3"),
    "release alt": Key("alt:up"),
    "(hold|press) shift": Key("shift:down"),
    "release shift": Key("shift:up"),
    "(hold|press) control": Key("ctrl:down/3"),
    "release control": Key("ctrl:up"),
    "release [all]": release,
    "angle brackets": Key("langle, rangle, left/3"),
    "brackets": Key("lbracket, rbracket, left/3"),
    "braces": Key("lbrace, rbrace, left/3"),
    "parens": Key("lparen, rparen, left/3"),
}


class KeystrokeRule(MappingRule):
    mapping = commands
    extras = [
        IntegerRef("n", 1, 100)
    ]
    defaults = {
        "n": 1,
    }


def create_grammar():
    grammar = Grammar("miscellaneous")
    grammar.add_rule(KeystrokeRule())
    grammar.add_rule(ActionRule())
    return grammar, True
