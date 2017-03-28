"""A command module for Dragonfly, for generic editing help.

-----------------------------------------------------------------------------
This is a heavily modified version of the _multiedit-en.py script at:
http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html  # @IgnorePep8
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""
from dragonfly import *
from dragonfly.actions.keyboard import keyboard
from dragonfly.actions.typeables import typeables

common_symbols = {
    "(dash|minus|hyphen)": "-",
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
}


class CommonSymbolRule(MappingRule):

    mapping = common_symbols

    def _process_recognition(self, node, extras):
        Text(node).execute()


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


class RareSymbolRule(CompoundRule):

    spec = "<symbol> (sign|symbol)"
    extras = [Choice("symbol", rare_symbols)]

    def _process_recognition(self, node, extras):
        symbol = extras["symbol"]
        Text(symbol).execute()


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


class SpellRule(CompoundRule):
    spec = "spell <symbols>"
    extras = [Repetition(name="symbols", child=Choice("symbols", all_symbols), max=20)]

    def _process_recognition(self, node, extras):
        Text(reduce(lambda x,y: x + y, extras["symbols"])).execute()


class LetterRule(CompoundRule):

    spec = "letter <letter>"
    extras = [Choice("letter", letter_map)]

    def _process_recognition(self, node, extras):
        letter = extras["letter"][0]
        Text(letter).execute()


class CapitalLetterRule(CompoundRule):

    spec = "(cap|capital) letter <letter>"
    extras = [Choice("letter", letter_map)]

    def _process_recognition(self, node, extras):
        letter = extras["letter"][1]
        Text(letter).execute()


class NumberRule(CompoundRule):

    spec = "number <m> [point <n>]"
    extras = [NumberRef("m", True), NumberRef("n", True)]

    def _process_recognition(self, node, extras):
        integer = extras["m"]
        number = str(integer)
        if "n" in extras:
            floating_point = extras["n"]
            number += "." + str(floating_point)

        Text(number).execute()


def create_grammar():
    grammar = Grammar("symbols")
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
