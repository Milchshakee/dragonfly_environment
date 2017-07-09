from dragonfly import *

from modules.command_tracker import key, func, text, mouse, sequence
from modules.util import formatter
from modules.util.dragonfly_utils import get_selected_text


def _change_visibility(prefix):
    mouse("left/3").execute()
    key("s-f6/20").execute()
    name = get_selected_text()
    if name.startswith("__"):
        name = name[2:]
    elif name.startswith("_"):
        name = name[1:]
    name = prefix + name
    text(name).execute()
    key("enter/3").execute()


mapping = {
    "import this": Mouse("left") + Key("a-enter"),
    # Code execution.
    "run app": Key("s-f10"),
    "re-run app": Key("c-f5"),
    "run test": Key("cs-f10"),
    "stop running": Key("c-f2"),

    # Code navigation.
    "go to declaration": Mouse("left") + Key("c-b"),
    "go to implementation": Mouse("left") + Key("ca-b"),
    "go to super": Mouse("left") + Key("c-u"),
    "go to (class|test)": Mouse("left") + Key("cs-t"),
    "go back": Mouse("left") + Key("ca-left"),

    # Project settings.
    "go to project window": Key("a-1"),
    "go to module settings": Key("f4"),
    "go to [project] settings": Key("ca-s"),
    "synchronize files": Key("ca-y"),

    # Terminal.
    "run terminal": Key("a-f12"),

    # Search.
    "find text": Key("c-f"),
    "find in path": Key("cs-f"),
    "find usages": Mouse("left") + Key("a-f7"),
    "replace text": Key("c-r"),

    # Edit.
    "(save|safe) [file|all]": Key("c-s"),

    # Code.
    "show intentions": Mouse("left") + Key("a-enter"),
    "accept choice": Key("c-enter"),
    "go to line": Key("c-g"),
    "go to line <n>": Key("c-g/25") + Text("%(n)d") + Key("enter"),
    "[go to] start of line": Key("home"),
    "[go to] end of line": Key("end"),
    "implement method": Key("c-i"),
    "override method": Key("c-o"),

    # Window handling.
    "next tab": Key("a-right"),
    "previous tab": Key("a-left"),
    "close tab": Key("c-f4"),

    # Version control.
    "git commit": Key("c-k"),
    "git update": Key("c-t"),
    "git add": Key("ca-a"),
    "git push": Key("cs-k"),
    "commit": Key("i"),
    "push": Key("p"),

    # Refactoring.
    "(refactor|re-factor) (this|choose)": Key("cas-t"),
    "(refactor|re-factor) rename": Key("s-f6"),
    "(refactor|re-factor) change signature": Key("c-f6"),
    "(refactor|re-factor) move": Key("f6"),
    "(refactor|re-factor) copy": Key("f5"),
    "(refactor|re-factor) safe delete": Key("a-del"),
    "(refactor|re-factor) extract variable": Key("ca-v"),
    "(refactor|re-factor) extract constant": Key("ca-c"),
    "(refactor|re-factor) extract field": Key("ca-f"),
    "(refactor|re-factor) extract parameter": Key("ca-p"),
    "(refactor|re-factor) extract method": Key("ca-m"),
    "(refactor|re-factor) (in line|inline)": Key("ca-n"),
    "make normal": func(_change_visibility, prefix=""),
    "make protected": func(_change_visibility, prefix="_"),
    "make private": func(_change_visibility, prefix="__"),

    "complete": Key("c-space"),
    "only <text>": sequence(func(formatter.format_and_write_text, format_type=formatter.FormatType.snakeCase),
                                     key("c-space/3")),
    "first <text>": sequence(func(formatter.format_and_write_text, format_type=formatter.FormatType.snakeCase),
                                     key("c-space/3, enter/3")),
    "option <n>": Key("down/3:%(n)d, up/3, enter"),
    "hide window": Mouse("left") + Key("s-escape"),
    "close search bar": Key("escape"),


    "new file": Mouse("right/3") + Key("down/3, right/3, enter"),
    "delete file": Mouse("left/3") + Key("delete"),
    "cancel": Key("escape")
}


class CommandRule(MappingRule):
    mapping = mapping

    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 50000)
    ]


def create_grammar():
    idea_context = AppContext(executable="pycharm")
    grammar = Grammar("pycharm", context=idea_context)
    grammar.add_rule(CommandRule())
    return grammar, True
