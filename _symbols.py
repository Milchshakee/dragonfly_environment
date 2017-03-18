"""A command module for Dragonfly, for generic editing help.

-----------------------------------------------------------------------------
This is a heavily modified version of the _multiedit-en.py script at:
http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html  # @IgnorePep8
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""
from dragonfly import *
from dragonfly.actions.keyboard import keyboard
from dragonfly.actions.typeables import typeables

if 'semicolon' not in typeables:
    typeables["semicolon"] = keyboard.get_typeable(char=';')

grammar = Grammar("symbols")

common_symbols = {
    "(bar|vertical bar|pipe)": "|",
    "(dash|minus|hyphen)": "-",
    "(dot|period)": ".",
    "comma": ",",
    "backslash": "\\",
    "underscore": "_",
    "(star|asterisk)": "*",
    "colon": ":",
    "(semicolon|semi-colon)": ";",
    "slash": "/",
    "space": " "
}


class CommonSymbolRule(MappingRule):

    mapping = common_symbols

    def _process_recognition(self, node, extras):
        Text(node).execute()

grammar.add_rule(CommonSymbolRule())

rare_symbols = {
    "at": "@",
    "[double] quote": '"',
    "single quote": "'",
    "hash": "#",
    "dollar": "$",
    "percent": "%",
    "and": "&",
    "equal": "=",
    "plus": "+"
}


class SymbolRule(CompoundRule):

    spec = "<symbol> (sign|symbol)"
    extras = [Choice("symbol", rare_symbols)]

    def _process_recognition(self, node, extras):
        symbol = extras["symbol"]
        Text(symbol).execute()

letter_map = {
    "(A|alpha)": ("a", "A"),
    "(B|bravo) ": ("b", "B"),
    "(C|charlie) ": ("c", "C"),
    "(D|delta) ": ("d", "D"),
    "(E|echo) ": ("e", "E"),
    "(F|foxtrot) ": ("f", "F"),
    "(G|golf) ": ("g", "G"),
    "(H|hotel) ": ("h", "H"),
    "(I|india|indigo) ": ("i", "I"),
    "(J|juliet) ": ("j", "J"),
    "(K|kilo) ": ("k", "K"),
    "(L|lima) ": ("l", "L"),
    "(M|mike) ": ("m", "M"),
    "(N|november) ": ("n", "N"),
    "(O|oscar) ": ("o", "O"),
    "(P|papa|poppa) ": ("p", "P"),
    "(Q|quebec|quiche) ": ("q", "Q"),
    "(R|romeo) ": ("r", "R"),
    "(S|sierra) ": ("s", "S"),
    "(T|tango) ": ("t", "T"),
    "(U|uniform) ": ("u", "U"),
    "(V|victor) ": ("v", "V"),
    "(W|whiskey) ": ("w", "W"),
    "(X|x-ray) ": ("x", "X"),
    "(Y|yankee) ": ("y", "Y"),
    "(Z|zulu) ": ("z", "Z")
}


class LetterRule(CompoundRule):

    spec = "letter <letter>"
    extras = [Choice("letter", letter_map)]

    def _process_recognition(self, node, extras):
        letter = extras["letter"][0]
        Text(letter).execute()

grammar.add_rule(LetterRule())


class CapitalLetterRule(CompoundRule):

    spec = "capital letter <letter>"
    extras = [Choice("letter", letter_map)]

    def _process_recognition(self, node, extras):
        letter = extras["letter"][1]
        Text(letter).execute()

grammar.add_rule(CapitalLetterRule())


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

grammar.add_rule(NumberRule())
grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
