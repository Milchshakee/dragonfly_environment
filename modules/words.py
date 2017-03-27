import os
from modules.util.json_parser import parse_file

from dragonfly import Grammar, Alternative, Text, Choice, Compound, MappingRule

abbreviation_map = {}
special_words = []

data = {
    "abbreviate <abbreviation>": Text("%(abbreviation)s"),
    "word <special_word>": Text("%(special_word)s"),
}

default_special_words = {"special_words": ["word1", "some text", "etc"]}


def reload_config(config_path):
    global abbreviation_map
    abbreviation_map = parse_file(os.path.join(config_path, "abbreviations.json"))["abbreviations"]
    global special_words
    special_words = parse_file(os.path.join(config_path, "special_words.json"), default_special_words)["special_words"]


def create_grammar():
    special_words_alternatives = [Compound(spec=word, value=word) for word in special_words]
    grammar = Grammar("words")
    grammar.add_rule(MappingRule(mapping=data, extras=[
        Alternative(name="special_word", children=special_words_alternatives),
        Choice("abbreviation", abbreviation_map)
    ]))
    return grammar, True
