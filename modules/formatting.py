from dragonfly import *
import command_tracker
from modules.util.formatter import format_map, FormatType, format_text

fallback_format = FormatType.spokenForm


def format_input(text, format_type):
    formatted = format_text(text, format_type)
    command_tracker.text(formatted).execute()


def change_fallback_format(format_type):
    global fallback_format
    fallback_format = format_type


command_map = {
    "set default format <format_type>": Function(change_fallback_format),
    "<format_type> <text>": Function(format_input),
    # "<text>": Function(format_input, format_type=fallback_format)
}


class FormatRule(MappingRule):
    mapping = command_map
    extras = [
        Dictation("text"),
        Choice("format_type", format_map),
    ]


def create_grammar():
    grammar = Grammar("formatting")
    grammar.add_rule(FormatRule())
    return grammar, True
