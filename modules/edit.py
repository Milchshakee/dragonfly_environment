from dragonfly import *
from mouse import stop_marking

shell_context = AppContext(executable="cmd") | AppContext(executable="powershell")
normal_context = ~shell_context


def select_string(include_quotes):
    Mouse("left/3").execute()
    Key("c-left, c-right").execute()

    clipboard = Clipboard()
    saved_text = clipboard.get_system_text()
    clipboard.set_system_text('')
    left_counter = 0
    while left_counter < 50:
        Key("s-left, c-c/3").execute()
        left_counter += 1
        if clipboard.get_system_text().startswith("\""):
            break

    Key("left").execute()
    move_right = left_counter
    if not include_quotes:
        move_right -= 1
        Key("right").execute()
    Key("s-right:%s" % move_right).execute()

    right_counter = 0
    while right_counter < 50:
        Key("s-right, c-c/3").execute()
        right_counter += 1
        if clipboard.get_system_text().endswith("\""):
            break

    if not include_quotes:
        Key("s-left").execute()

    clipboard.set_text(saved_text)
    clipboard.copy_to_system()

actions = {
    "cut": Key("c-x/3"),
    "copy": Key("c-c/3"),
    "replace": Key("c-v/3"),
    "delete": Key("del/3"),
    "select": Text("")
}

scopes = {
    "all": Key("c-a/3"),
    "line": Mouse("left/3, left/3, left/3"),
    "this": Mouse("left/3, left/3"),
    "string": Function(select_string, include_quotes=True),
    "string content": Function(select_string, include_quotes=False),
    "[selection]": Function(stop_marking)
}


class NormalActionRule(CompoundRule):
    spec = "<action> <scope>"
    extras = [
        Choice("action", actions),
        Choice("scope", scopes)
    ]

    def _process_recognition(self, node, extras):
        action = extras["action"]
        scope = extras["scope"]
        scope.execute()
        Pause("3").execute()
        action.execute()

normal_data = {
    "clear line": scopes["line"] + actions["delete"] + Key("enter/3, up/3"),
    "delete <n>": Function(stop_marking) + Key("del/3:%(n)d"),
    "delete here <n>": Mouse("left") + Function(stop_marking) + Key("del/3:%(n)d"),
    "(back|backspace) [<n>]": Key("backspace/1:%(n)d"),
    "(back|backspace) here [<n>]": Mouse("left") + Key("backspace/1:%(n)d"),
    "paste": Key("c-v/3"),
    "paste here": Mouse("left") + Key("c-v/3"),
}

shell_data = {
    "copy": Function(stop_marking) + Key("enter"),
    "delete <n>": Key("del/3:%(n)d"),
    "(back|backspace) [<n>]": Key("backspace/1:%(n)d"),
    "paste": Mouse("right"),
}


class KeystrokeRule(MappingRule):
    extras = [
        IntegerRef("n", 1, 100)
    ]
    defaults = {
        "n": 1,
    }

    def __init__(self, name, mapping, context):
        MappingRule.__init__(self, name=name, mapping=mapping, context=context)


def create_grammar():
    grammar = Grammar("edit")
    grammar.add_rule(KeystrokeRule("shell", shell_data, shell_context))
    grammar.add_rule(KeystrokeRule("normal", normal_data, normal_context))
    grammar.add_rule(NormalActionRule())
    return grammar, True
