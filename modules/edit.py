from modules.util.dragonfly_utils import get_unique_rule_name
from modules.util.utils import shell_context, normal_context
from dragonfly import *
import global_state


def select_string(include_quotes):
    Mouse("left/3").execute()
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
    "cut": (Key("c-x/3"), False),
    "copy": (Key("c-c/3"), True),
    "replace": (Key("c-v/3"), False),
    "delete": (Key("del/3"), False),
    "select": (Text(""), True),
}

scopes = {
    "all": Key("c-a/3"),
    "line": Mouse("left/3, left/3, left/3"),
    "line content": Mouse("left/3") + Key("home/3, s-end/3"),
    "this": Mouse("left/3, left/3"),
    "string": Function(select_string, include_quotes=True),
    "string content": Function(select_string, include_quotes=False),
    "letter": Mouse("left/3") + Key("s-right/3"),
    "left": Mouse("left/3") + Key("s-home"),
    "right": Mouse("left/3") + Key("s-end")

}


class NormalActionRule(CompoundRule):
    spec = "<action> [<scope>]"
    extras = [
        Choice("action", actions),
        Choice("scope", scopes)
    ]

    def _process_recognition(self, node, extras):
        action, retains_mark = extras["action"]
        if "scope" in extras:
            scope = extras["scope"]
            scope.execute()
        else:
            global_state.stop_marking()

        if retains_mark:
            global_state.is_something_marked = True

        Pause("3").execute()
        action.execute()


def remove_mark_or_update_cursor():
    if global_state.is_marking:
        global_state.stop_marking()
    elif global_state.is_something_marked:
        global_state.is_something_marked = False
    elif global_state.get_complete_nesting_level() == 0:
        global_state.update_cursor()


def indent(n):
    if global_state.is_marking:
        global_state.stop_marking()
        Key("tab:%s" % n).execute()
    elif global_state.is_something_marked:
        Key("tab:%s" % n).execute()
    else:
        global_state.update_cursor()
        Key("home, tab:%s" % n).execute()


def unindent(n):
    Key("shift:down/3").execute()

    if global_state.is_marking:
        global_state.stop_marking()
        Key("tab:%s" % n).execute()
    elif global_state.is_something_marked:
        Key("tab:%s" % n).execute()
    else:
        global_state.update_cursor()
        Key("tab:%s" % n).execute()

    Key("shift:up/3").execute()

normal_data = {
    "select": scopes["this"] + actions["select"][0],
    "delete <n>": Function(remove_mark_or_update_cursor) + Key("del/3:%(n)d"),
    "(back|backspace) [<n>]": Function(remove_mark_or_update_cursor) + Key("backspace/1:%(n)d"),
    "paste": Function(remove_mark_or_update_cursor) + Key("c-v/3"),

    "(new-line | new line) [<n>]": Function(remove_mark_or_update_cursor) + Key("end/3, enter/3:%(n)d"),
    "(new-line | new line) [<n>] here": Function(remove_mark_or_update_cursor) + Key("enter/3:%(n)d"),
    "indent [<n>]": Function(indent),
    "unindent [<n>]": Function(unindent),

    "undo": Key("c-z/3"),
    "undo <n> [times]": Key("c-z/3:%(n)d"),
    "redo": Key("c-y/3"),
    "redo <n> [times]": Key("c-y/3:%(n)d"),

}

shell_data = {
    "copy": Function(global_state.stop_marking) + Key("enter"),
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

    def __init__(self, mapping, context):
        MappingRule.__init__(self, name=get_unique_rule_name(), mapping=mapping, context=context)


def create_grammar():
    grammar = Grammar("edit")
    grammar.add_rule(KeystrokeRule(shell_data, shell_context))
    grammar.add_rule(KeystrokeRule(normal_data, normal_context))
    grammar.add_rule(NormalActionRule())
    return grammar, True
