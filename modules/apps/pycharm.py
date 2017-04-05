from dragonfly import *

import modules.util.formatter

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
    "(refactor|re-factor) extract variable": Key("ca-v"),
    "(refactor|re-factor) extract method": Key("ca-m"),
    "(refactor|re-factor) (in line|inline)": Key("ca-n"),

    "complete": Key("c-space"),
    "option <n>": Key("down/3:%(n)d, up/3, enter"),
    "hide window": Mouse("left") + Key("s-escape"),
    "close search bar": Key("escape"),
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
