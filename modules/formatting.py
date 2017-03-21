from dragonfly import *

from modules.util.formatter import (
    camel_case_count,
    pascal_case_count,
    snake_case_count,
    squash_count,
    expand_count,
    uppercase_count,
    lowercase_count,
    format_text,
    FormatTypes as ft,
)

formatMap = {
    "camel case": ft.camelCase,
    "pascal case": ft.pascalCase,
    "snake case": ft.snakeCase,
    "uppercase": ft.upperCase,
    "lowercase": ft.lowerCase,
    "squash": ft.squash,
    "lowercase squash": [ft.squash, ft.lowerCase],
    "uppercase squash": [ft.squash, ft.upperCase],
    "squash lowercase": [ft.squash, ft.lowerCase],
    "squash uppercase": [ft.squash, ft.upperCase],
    "dashify": ft.dashify,
    "lowercase dashify": [ft.dashify, ft.lowerCase],
    "uppercase dashify": [ft.dashify, ft.upperCase],
    "dashify lowercase": [ft.dashify, ft.lowerCase],
    "dashify uppercase": [ft.dashify, ft.upperCase],
    "dotify": ft.dotify,
    "lowercase dotify": [ft.dotify, ft.lowerCase],
    "uppercase dotify": [ft.dotify, ft.upperCase],
    "dotify lowercase": [ft.dotify, ft.lowerCase],
    "dotify uppercase": [ft.dotify, ft.upperCase],
    "say": ft.spokenForm,
    "environment variable": [ft.snakeCase, ft.upperCase],
}

command_map = {
    "underscore [<n>]": Key("underscore/2:%(n)d"),
    "camel case <n> [words]": Function(camel_case_count),
    "pascal case <n> [words]": Function(pascal_case_count),
    "snake case <n> [words]": Function(snake_case_count),
    "squash <n> [words]": Function(squash_count),
    "expand <n> [words]": Function(expand_count),
    "uppercase <n> [words]": Function(uppercase_count),
    "lowercase <n> [words]": Function(lowercase_count),
    "<format_type> <text>": Function(format_text),
    "say <text>": Text("%(text)s")
}


class FormatRule(MappingRule):
    mapping = command_map
    extras = [
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("format_type", formatMap),
    ]
    defaults = {
        "n": 1,
    }


def create_grammar():
    grammar = Grammar("formatting")
    grammar.add_rule(FormatRule())
    return grammar, True
