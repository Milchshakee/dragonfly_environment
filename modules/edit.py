from modules.command_tracker import mouse, sequence, key, func, reversible
from modules.util.dragonfly_utils import get_unique_rule_name
from modules.util.utils import shell_context, normal_context
from dragonfly import Clipboard, CompoundRule, Choice, MappingRule, IntegerRef, Grammar
import global_state


def select_string(include_quotes):
    mouse("left/3").execute()
    clipboard = Clipboard()
    saved_text = clipboard.get_system_text()
    clipboard.set_system_text('')
    left_counter = 0
    while left_counter < 50:
        key("s-left, c-c/3").execute()
        left_counter += 1
        if clipboard.get_system_text().startswith("\""):
            break

    key("left").execute()
    move_right = left_counter
    if not include_quotes:
        move_right -= 1
        key("right").execute()
    key("s-right:%s" % move_right).execute()

    right_counter = 0
    while right_counter < 50:
        key("s-right, c-c/3").execute()
        right_counter += 1
        if clipboard.get_system_text().endswith("\""):
            break

    if not include_quotes:
        key("s-left").execute()

    clipboard.set_text(saved_text)
    clipboard.copy_to_system()


def _select():
    global_state.is_something_marked = True


class Action:
    cut = key("c-x/3")
    copy = key("c-c/3, left/3")
    replace = key("c-v/3")
    delete = key("del/3")
    select = func(_select)

_actions = {
    "cut": Action.cut,
    "copy": Action.copy,
    "replace": Action.replace,
    "delete": Action.delete,
    "select": Action.select,
}


class Scope:
    all = key("c-a/3")
    line = mouse("left/3, left/3, left/3")
    line_content = sequence(mouse("left/3"), key("home/3, s-end/3"))
    this = mouse("left/3, left/3")
    string = func(select_string, include_quotes=True)
    string_content = func(select_string, include_quotes=False)
    letter = sequence(mouse("left/3"), key("s-right/3"))
    left = sequence(mouse("left/3"), key("s-home/3"))
    right = sequence(mouse("left/3"), key("s-end/3"))

_scopes = {
    "all": Scope.all,
    "line": Scope.line,
    "line content": Scope.line_content,
    "this": Scope.this,
    "string": Scope.string,
    "string content": Scope.string_content,
    "letter": Scope.letter,
    "left": Scope.left,
    "right": Scope.right
}


def edit(action, scope):
    if global_state.is_marking:
        global_state.stop_marking()
    elif global_state.is_something_marked:
        global_state.is_something_marked = False
    elif scope is None:
        print()

    if scope is not None:
        scope.execute()

    if action is not None:
        action.execute()


class NormalActionRule(CompoundRule):
    spec = "<action> [<scope>]"
    extras = [
        Choice("action", _actions),
        Choice("scope", _scopes)
    ]

    def _process_recognition(self, node, extras):
        action = extras["action"]
        scope = None
        if "scope" in extras:
            scope = extras["scope"]
        edit(action, scope)


def update_cursor():
    if global_state.is_cursor_following_mouse:
        mouse("left/3").execute()


def remove_mark_or_update_cursor():
    if global_state.is_marking:
        global_state.stop_marking()
    elif global_state.is_something_marked:
        global_state.is_something_marked = False
    elif global_state.get_complete_nesting_level() == 0:
        update_cursor()


def indent(n):
    if global_state.is_marking:
        global_state.stop_marking()
        key("tab:%s" % n).execute()
    elif global_state.is_something_marked:
        key("tab:%s" % n).execute()
    else:
        update_cursor()
        key("home/3, tab:%s" % n).execute()


def unindent(n):
    key("shift:down/3").execute()

    if global_state.is_marking:
        global_state.stop_marking()
        key("tab:%s" % n).execute()
    elif global_state.is_something_marked:
        key("tab:%s" % n).execute()
    else:
        update_cursor()
        key("tab:%s" % n).execute()

    key("shift:up/3").execute()

normal_data = {
    "select": func(edit, action=Action.select, scope=Scope.this),
    "delete <n>": sequence(func(remove_mark_or_update_cursor), key("del/3:%(n)d")),
    "(back|backspace) [<n>]": sequence(func(remove_mark_or_update_cursor), key("backspace/1:%(n)d")),
    "paste": sequence(func(remove_mark_or_update_cursor), key("c-v/3")),

    "(new-line | new line) [<n>]": sequence(func(remove_mark_or_update_cursor), key("end/3, enter/3:%(n)d")),
    "(new-line | new line) [<n>] here": sequence(func(remove_mark_or_update_cursor), key("enter/3:%(n)d")),
    "indent [<n>]": reversible(func(indent), func(unindent)),
    "unindent [<n>]": reversible(func(unindent), func(indent)),

    "undo": key("c-z/3"),
    "undo <n> [times]": key("c-z/3:%(n)d"),
    "redo": key("c-y/3"),
    "redo <n> [times]": key("c-y/3:%(n)d"),

}

shell_data = {
    "copy": func(global_state.stop_marking) + key("enter"),
    "delete <n>": key("del/3:%(n)d"),
    "(back|backspace) [<n>]": key("backspace/1:%(n)d"),
    "paste": mouse("right"),
}


class keystrokeRule(MappingRule):
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
    grammar.add_rule(keystrokeRule(shell_data, shell_context))
    grammar.add_rule(keystrokeRule(normal_data, normal_context))
    grammar.add_rule(NormalActionRule())
    return grammar, True
