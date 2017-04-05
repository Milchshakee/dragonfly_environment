from dragonfly import *
from dragonfly.actions.keyboard import keyboard
from dragonfly.actions.typeables import typeables
from modules.util.dragonfly_utils import PositionalText, SurroundRule

common_symbols = {
    "(dash)": "-",
    "(dot|period)": ".",
    "comma": ",",
    "backslash": "\\",
    "underscore": "_",
    "(star|asterisk)": "*",
    "colon": ":",
    "(semicolon|semi-colon)": ";",
    "slash": "/",
    "space": " ",
    "[double] quote": '"',
    "single quote": "'",
    "open paren": "(",
    "close paren": ")",
    "open bracket": "[",
    "close bracket": "]",
    "open angle bracket": "<",
    "close angle bracket": ">",
    "open brace": "{",
    "close brace": "}",
    "tab": "    "
}


surroundings = {
    "angle brackets": ("<", ">"),
    "brackets": ("[", "]"),
    "braces": ("{", "}"),
    "parens": ("(", ")"),
    "[double] quotes": ("\"", "\""),
    "single quotes": ("'", "'"),
}


rare_symbols = {
    "at": "@",
    "hash": "#",
    "dollar": "$",
    "percent": "%%",
    "and": "&",
    "equal": "=",
    "plus": "+",
    "(bar|vertical bar|pipe)": "|",
    "caret": "^"
}


letter_map = {
    "(alpha)": ("a", "A"),
    "(bravo) ": ("b", "B"),
    "(charlie) ": ("c", "C"),
    "(delta) ": ("d", "D"),
    "(echo) ": ("e", "E"),
    "(foxtrot) ": ("f", "F"),
    "(golf) ": ("g", "G"),
    "(hotel) ": ("h", "H"),
    "(india|indigo) ": ("i", "I"),
    "(juliet) ": ("j", "J"),
    "(kilo) ": ("k", "K"),
    "(lima) ": ("l", "L"),
    "(mike) ": ("m", "M"),
    "(November) ": ("n", "N"),
    "(oscar) ": ("o", "O"),
    "(papa|poppa) ": ("p", "P"),
    "(Quebec|quiche) ": ("q", "Q"),
    "(romeo) ": ("r", "R"),
    "(sierra) ": ("s", "S"),
    "(tango) ": ("t", "T"),
    "(uniform) ": ("u", "U"),
    "(victor) ": ("v", "V"),
    "(whiskey) ": ("w", "W"),
    "(x-ray) ": ("x", "X"),
    "(yankee) ": ("y", "Y"),
    "(Zulu) ": ("z", "Z")
}

all_symbols = {}
for key, value in letter_map.iteritems():
    all_symbols[key] = letter_map[key][0]
    all_symbols["(cap|capital) " + key] = letter_map[key][1]
all_symbols.update(common_symbols)
all_symbols.update(rare_symbols)


class CommonSymbolRule(MappingRule):

    mapping = common_symbols

    def _process_recognition(self, node, extras):
        PositionalText(node).execute()



class RareSymbolRule(CompoundRule):

    spec = "<symbol> (sign|symbol)"
    extras = [Choice("symbol", rare_symbols)]

    def _process_recognition(self, node, extras):
        symbol = extras["symbol"]
        PositionalText(symbol).execute()


class SpellRule(CompoundRule):
    spec = "spell <symbols>"
    extras = [Repetition(name="symbols", child=Choice("symbols", all_symbols), max=20)]

    def _process_recognition(self, node, extras):
        PositionalText(reduce(lambda x, y: x + y, extras["symbols"])).execute()


class LetterRule(CompoundRule):

    spec = "letter <letter>"
    extras = [Choice("letter", letter_map)]

    def _process_recognition(self, node, extras):
        letter = extras["letter"][0]
        PositionalText(letter).execute()


class CapitalLetterRule(CompoundRule):

    spec = "(cap|capital) letter <letter>"
    extras = [Choice("letter", letter_map)]

    def _process_recognition(self, node, extras):
        letter = extras["letter"][1]
        PositionalText(letter).execute()


class NumberRule(CompoundRule):

    spec = "number <m> [point <n>]"
    extras = [NumberRef("m", True), NumberRef("n", True)]

    def _process_recognition(self, node, extras):
        integer = extras["m"]
        number = str(integer)
        if "n" in extras:
            floating_point = extras["n"]
            number += "." + str(floating_point)

        PositionalText(number).execute()


def create_grammar():
    grammar = Grammar("symbols")
    for key, value in surroundings.iteritems():
        grammar.add_rule(SurroundRule(key, value[0], value[1]))
    grammar.add_rule(SpellRule())
    grammar.add_rule(CommonSymbolRule())
    grammar.add_rule(RareSymbolRule())
    grammar.add_rule(LetterRule())
    grammar.add_rule(CapitalLetterRule())
    grammar.add_rule(NumberRule())
    return grammar, True


def load():
    if 'semicolon' not in typeables:
        typeables["semicolon"] = keyboard.get_typeable(char=';')
