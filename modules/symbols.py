from dragonfly import *

from modules.command_tracker import text, surround_rule, key

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
    "(a|alpha)": ("a", "A"),
    "(be|bravo) ": ("b", "B"),
    "(see|charlie) ": ("c", "C"),
    "(di|delta) ": ("d", "D"),
    "(ihh|echo) ": ("e", "E"),
    "(eff|foxtrot) ": ("f", "F"),
    "(gee|golf) ": ("g", "G"),
    "(h|hotel) ": ("h", "H"),
    "(I|india|indigo) ": ("i", "I"),
    "(jay|juliet) ": ("j", "J"),
    "(kay|kilo) ": ("k", "K"),
    "(ell|lima) ": ("l", "L"),
    "(em|mike) ": ("m", "M"),
    "(en|November) ": ("n", "N"),
    "(oh|oscar) ": ("o", "O"),
    "(pee|papa|poppa) ": ("p", "P"),
    "(q|quebec|quiche) ": ("q", "Q"),
    "(r|romeo) ": ("r", "R"),
    "(s|sierra) ": ("s", "S"),
    "(tee|tango) ": ("t", "T"),
    "(you|uniform) ": ("u", "U"),
    "(v|victor) ": ("v", "V"),
    "(w|whiskey) ": ("w", "W"),
    "(ex|x-ray) ": ("x", "X"),
    "(why|yankee) ": ("y", "Y"),
    "(zat|Zulu) ": ("z", "Z")
}

all_symbols = {}
for k, v in letter_map.iteritems():
    all_symbols[k] = v[0]
    all_symbols["(cap|capital) " + k] = v[1]
all_symbols.update(common_symbols)
all_symbols.update(rare_symbols)


class CommonSymbolRule(MappingRule):

    mapping = common_symbols

    def _process_recognition(self, node, extras):
        text(node).execute()


class RareSymbolRule(CompoundRule):

    spec = "<symbol> (sign|symbol)"
    extras = [Choice("symbol", rare_symbols)]

    def _process_recognition(self, node, extras):
        symbol = extras["symbol"]
        text(symbol).execute()


class SpellRule(CompoundRule):
    spec = "spell <symbols>"
    extras = [Repetition(name="symbols", child=Choice("symbols", all_symbols), max=20)]

    def _process_recognition(self, node, extras):
        text(reduce(lambda x, y: x + y, extras["symbols"])).execute()


class LetterRule(CompoundRule):

    spec = "letter <letter>"
    extras = [Choice("letter", letter_map)]

    def _process_recognition(self, node, extras):
        letter = extras["letter"][0]
        text(letter).execute()


class CapitalLetterRule(CompoundRule):

    spec = "(cap|capital) letter <letter>"
    extras = [Choice("letter", letter_map)]

    def _process_recognition(self, node, extras):
        letter = extras["letter"][1]
        text(letter).execute()


class NumberRule(CompoundRule):

    spec = "number <m> [point <n>]"
    extras = [NumberRef("m", True), NumberRef("n", True)]

    def _process_recognition(self, node, extras):
        integer = extras["m"]
        number = str(integer)
        if "n" in extras:
            floating_point = extras["n"]
            number += "." + str(floating_point)

        text(number).execute()


def create_grammar():
    grammar = Grammar("symbols")
    for key, value in surroundings.iteritems():
        grammar.add_rule(surround_rule(key, value[0], value[1]))
    grammar.add_rule(SpellRule())
    grammar.add_rule(CommonSymbolRule())
    grammar.add_rule(RareSymbolRule())
    grammar.add_rule(LetterRule())
    grammar.add_rule(CapitalLetterRule())
    grammar.add_rule(NumberRule())
    return grammar, True
