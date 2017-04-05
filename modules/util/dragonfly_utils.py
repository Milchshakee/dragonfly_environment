from dragonfly import Clipboard, CompoundRule, Rule
from dragonfly import Key
from dragonfly.grammar.elements_compound import Compound
from modules.global_state import stop_marking, update_cursor
from dragonfly.actions.action_text import Text

import modules.global_state as global_state


__rule_counter = 0


def get_unique_rule_name():
    global __rule_counter
    __rule_counter += 1
    return str(__rule_counter)


def get_selected_text():
    clipboard = Clipboard()
    previous = clipboard.get_system_text()
    clipboard.set_system_text("")
    Key("c-c/3").execute()
    selected = clipboard.get_system_text()
    clipboard.set_text(previous)
    clipboard.copy_to_system()
    return selected


def set_clipboard(text):
    clipboard = Clipboard()
    clipboard.set_text(text)
    clipboard.copy_to_system()


class SurroundRule(Rule):

    def __init__(self, spec, start, end):
        self.__start = start
        self.__end = end
        child = Compound("[empty] " + spec)
        Rule.__init__(self, get_unique_rule_name(), child, exported=True)

    def process_recognition(self, node):
        is_empty = node.words()[0] == "empty"
        if global_state.is_marking:
            stop_marking()
            global_state.is_something_marked = True

        if global_state.is_something_marked:
            global_state.is_something_marked = False
            if is_empty:
                Text(self.__start + self.__end).execute()
            else:
                selected = get_selected_text()
                surrounded = self.__start + selected + self.__end
                set_clipboard(surrounded)
                Key("c-v/3").execute()
        else:
            PositionalText(self.__start + self.__end).execute()
            if not is_empty:
                offset = len(self.__end)
                global_state.add_nesting_level(offset)


class PositionalText(Text):

    def __init__(self, spec=None, static=False, pause=Text._pause_default, autofmt=False):
        Text.__init__(self, spec=spec, static=static, pause=pause, autofmt=autofmt)

    def _execute_events(self, events):
        if global_state.is_dictating:
            global_state.append_dictation(self._spec)
            return True
        else:
            if global_state.is_marking:
                stop_marking()
            elif global_state.is_something_marked:
                global_state.is_something_marked = False
            elif global_state.get_complete_nesting_level() == 0:
                update_cursor()
            return Text._execute_events(self, events)
