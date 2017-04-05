import os

from modules.util.dragonfly_utils import PositionalText, get_unique_rule_name
from modules.util.json_parser import parse_file
from dragonfly import Grammar, Alternative, Dictation, Choice, Compound, MappingRule, CompoundRule, RuleRef, Function

abbreviation_map = {}
special_words = {}


class AbbreviationRule(CompoundRule):

    spec = "abbreviate <abbreviation>"

    def __init__(self, exported):
        extras = [Choice("abbreviation", abbreviation_map)]
        CompoundRule.__init__(self, name=get_unique_rule_name(), extras=extras, exported=exported)

    def value(self, node):
        return node.get_child_by_name("abbreviation").value()

    def _process_recognition(self, node, extras):
        PositionalText(self.value(node)).execute()


class SpecialWordRule(CompoundRule):
    spec = "word <special_word>"

    def __init__(self, exported):
        extras = [Choice("special_word", special_words)]
        CompoundRule.__init__(self, name=get_unique_rule_name(), extras=extras, exported=exported)

    def value(self, node):
        return node.get_child_by_name("special_word").value()

    def _process_recognition(self, node, extras):
        PositionalText(self.value(node)).execute()


class CapitalizeRule(CompoundRule):

    spec = "(cap|capitalize) <word>"

    def __init__(self, exported):
        extras = [Alternative(name="word", children=[
            RuleRef(AbbreviationRule(False)),
            RuleRef(SpecialWordRule(False)),
            Dictation()
        ])]
        CompoundRule.__init__(self, name=get_unique_rule_name(), extras=extras, exported=exported)

    def value(self, node):
        value = str(node.get_child_by_name("word").value())
        return value[0:1].upper() + value[1:]

    def _process_recognition(self, node, extras):
        PositionalText(self.value(node)).execute()


class PluralRule(MappingRule):
    mapping = {
        "plural": PositionalText("s")
    }

    def __init__(self, exported):
        MappingRule.__init__(self, name=get_unique_rule_name(), exported=exported)

rules = None

default_special_words = {
    "special_words": {
        "some word": "some word",
        "some other word": "value"
    }
}



def load_config(config_path):
    global abbreviation_map
    abbreviation_map = parse_file(os.path.join(config_path, "abbreviations.json"))["abbreviations"]
    global special_words
    special_words = parse_file(os.path.join(config_path, "special_words.json"), default_special_words)["special_words"]


def post_config():
    global rules
    rules = [AbbreviationRule(False), SpecialWordRule(False), CapitalizeRule(False), PluralRule(False)]


def create_grammar():
    grammar = Grammar("words")
    grammar.add_rule(AbbreviationRule(True))
    grammar.add_rule(SpecialWordRule(True))
    grammar.add_rule(PluralRule(True))
    grammar.add_rule(CapitalizeRule(True))
    return grammar, True
