import os

from dragonfly import MappingRule, Key, Choice, Grammar
from modules.util.json_parser import parse_file


icon_indices = {}


class IconRule(MappingRule):

    mapping = {
        "[open] <icon> icon": Key("enter"),
        "open <icon> menu": Key("apps"),
    }

    def __init__(self):
        MappingRule.__init__(self, extras=[Choice("icon", icon_indices)])

    def _process_recognition(self, value, extras):
        count = extras["icon"] + 1
        action = Key("w-b/10, right:%d/10" % count) + value
        action.execute()


default_configuration = {
    "icons": [
        "some program",
        "some other program",
        "etc"
    ]
}


def load_config(config_path):
    global icon_indices
    icons = parse_file(os.path.join(config_path, "icons.json"), default_configuration)["icons"]
    for index, name in enumerate(icons):
        icon_indices[name] = index


def create_grammar():
    grammar = Grammar("icons")
    grammar.add_rule(IconRule())
    grammar.load()
    return grammar, True

