"""A command module for Dragonfly, for generic editing help.

-----------------------------------------------------------------------------
This is a heavily modified version of the _multiedit-en.py script at:
http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html  # @IgnorePep8
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""
from dragonfly import *
from _mouse_control import stop_marking

grammar = Grammar("common commands")

abbreviationMap = {
    "administrator": "admin",
    "administrators": "admins",
    "application": "app",
    "applications": "apps",
    "argument": "arg",
    "arguments": "args",
    "attribute": "attr",
    "attributes": "attrs",
    "(authenticate|authentication)": "auth",
    "binary": "bin",
    "button": "btn",
    "class": "cls",
    "command": "cmd",
    "(config|configuration)": "cfg",
    "context": "ctx",
    "control": "ctrl",
    "database": "db",
    "(define|definition)": "def",
    "description": "desc",
    "(develop|development)": "dev",
    "(dictionary|dictation)": "dict",
    "(direction|directory)": "dir",
    "dynamic": "dyn",
    "example": "ex",
    "execute": "exec",
    "exception": "exc",
    "expression": "exp",
    "(extension|extend)": "ext",
    "function": "func",
    "framework": "fw",
    "(initialize|initializer)": "init",
    "instance": "inst",
    "integer": "int",
    "iterate": "iter",
    "java archive": "jar",
    "javascript": "js",
    "keyword": "kw",
    "keyword arguments": "kwargs",
    "language": "lng",
    "library": "lib",
    "length": "len",
    "number": "num",
    "object": "obj",
    "okay": "ok",
    "package": "pkg",
    "parameter": "param",
    "parameters": "params",
    "pixel": "px",
    "position": "pos",
    "point": "pt",
    "previous": "prev",
    "property": "prop",
    "python": "py",
    "query string": "qs",
    "reference": "ref",
    "references": "refs",
    "(represent|representation)": "repr",
    "regular (expression|expressions)": "regex",
    "request": "req",
    "revision": "rev",
    "ruby": "rb",
    "session aidee": "sid",  # "session id" didn't work for some reason.
    "source": "src",
    "(special|specify|specific|specification)": "spec",
    "standard": "std",
    "standard in": "stdin",
    "standard out": "stdout",
    "string": "str",
    "(synchronize|synchronous)": "sync",
    "system": "sys",
    "utility": "util",
    "utilities": "utils",
    "temporary": "tmp",
    "text": "txt",
    "value": "val",
    "window": "win",
}

release = Key("shift:up, ctrl:up, alt:up")
end_marking = Function(stop_marking)


def reload_natlink():
    """Reloads Natlink and custom Python modules."""
    win = Window.get_foreground()
    FocusWindow(executable="natspeak").execute()
    Pause("10").execute()
    Key("a-f, r").execute()
    Pause("10").execute()
    win.set_foreground()


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
    "doc home": Key("c-home/3"),
    "doc end": Key("c-end/3"),
    "space": release + Key("space"),
    "space [<n>]": release + Key("space:%(n)d"),
    "enter [<n>]": release + Key("enter:%(n)d"),
    "tab [<n>]": Key("tab:%(n)d"),
    "delete": end_marking + Key("del"),
    "delete <n>": Key("del/3:%(n)d"),
    "delete [this] line": Key("home, s-end, del"),  # @IgnorePep8
    "(back|backspace) [<n>]": release + Key("backspace:%(n)d"),
    "application key": release + Key("apps/3"),
    "win key": release + Key("win/3"),
    "paste [that]": end_marking + Function(paste_command),
    "paste [that] here": Mouse("left") + Function(paste_command),
    "copy [that]": end_marking + Function(copy_command),
    "cut [that]": end_marking + Key("c-x/3"),
    "select all": release + Key("c-a/3"),

    "undo": release + Key("c-z/3"),
    "undo <n> [times]": release + Key("c-z/3:%(n)d"),
    "redo": release + Key("c-y/3"),
    "redo <n> [times]": release + Key("c-y/3:%(n)d"),

    "[(hold|press)] alt": Key("alt:down/3"),
    "release alt": Key("alt:up"),
    "[(hold|press)] shift": Key("shift:down"),
    "release shift": Key("shift:up"),
    "[(hold|press)] control": Key("ctrl:down/3"),
    "release control": Key("ctrl:up"),
    "release [all]": release,
    "angle brackets": Key("langle, rangle, left/3"),
    "brackets": Key("lbracket, rbracket, left/3"),
    "braces": Key("lbrace, rbrace, left/3"),
    "parens": Key("lparen, rparen, left/3"),
    "abbreviate <abbreviation>": Text("%(abbreviation)s"),
    "reload Natlink": Function(reload_natlink),
}


class KeystrokeRule(MappingRule):
    exported = False
    mapping = commands
    extras = [
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Dictation("text2"),
        Choice("abbreviation", abbreviationMap)
    ]
    defaults = {
        "n": 1,
    }

grammar.add_rule(KeystrokeRule())
grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
