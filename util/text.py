import re

from dragonfly import Text
from dragonfly.actions.keyboard import Keyboard


letterMap = {
    "A\\letter": "alpha",
    "B\\letter": "bravo",
    "C\\letter": "charlie",
    "D\\letter": "delta",
    "E\\letter": "echo",
    "F\\letter": "foxtrot",
    "G\\letter": "golf",
    "H\\letter": "hotel",
    "I\\letter": "india",
    "J\\letter": "juliet",
    "K\\letter": "kilo",
    "L\\letter": "lima",
    "M\\letter": "mike",
    "N\\letter": "november",
    "O\\letter": "oscar",
    "P\\letter": "papa",
    "Q\\letter": "quebec",
    "R\\letter": "romeo",
    "S\\letter": "sierra",
    "T\\letter": "tango",
    "U\\letter": "uniform",
    "V\\letter": "victor",
    "W\\letter": "whiskey",
    "X\\letter": "x-ray",
    "Y\\letter": "yankee",
    "Z\\letter": "zulu",
}


def extract_dragon_info(input_text):
    newWords = []
    words = str(input_text).split(" ")
    for word in words:
        if word in letterMap.keys():
            word = letterMap[word]
        elif word.rfind("\\") > -1:
            pos = word.rfind("\\") + 1
            if (len(word) - 1) >= pos:
                word = word[pos:]  # Remove written form info.
            else:
                word = ""
        newWords.append(word)
    return newWords


specialCharacterTranslations = {
    "?\\question-mark": "?",
    ":\\colon": ":",
    ";\\semicolon": ";",
    "*\\asterisk": "*",
    "~\\tilde": "~",
    ",\\comma": ",",
    ".\\period": ".",
    ".\\dot": ".",
    "/\\slash": "/",
    "_\\underscore": "_",
    "!\\exclamation-mark": "!",
    "@\\at-sign": "@",
    "\\backslash": "\\",
    "(\\left-parenthesis": "(",
    ")\\right-parenthesis": ")",
    "[\\left-square-bracket": "[",
    "]\\right-square-bracket": "]",
    "{\\left-curly-bracket": "{",
    "}\\right-curly-bracket": "}",
    "<\\left-angle-bracket": "<",
    ">\\right-angle-bracket": ">",
    "|\\vertical-bar": "|",
    "$\\dollar-sign": "$",
    "=\\equals-sign": "=",
    "+\\plus-sign": "+",
    "-\\minus-sign": "-",
    "--\\dash": "-",
    "\x96\\dash": "-",
    "-\\hyphen": "-",
    "\"\\right-double-quote": "\"",
    "\"\\left-double-quote": "\"",
}

specialCharacterTranslationsRe = re.compile('|'.join(re.escape(key) for key in specialCharacterTranslations.keys()))


def strip_dragon_info(text):
    newWords = []
    words = str(text).split(" ")
    for word in words:
        word = specialCharacterTranslationsRe.sub(lambda m: specialCharacterTranslations[m.group()], word)

        backslash_index = word.find("\\")
        if backslash_index > -1:
            word = word[:backslash_index]  # Remove spoken form info.
        newWords.append(word)
    return newWords


class SCText(Text):  # Special Characters Text.
    def __init__(self, spec=None, static=False, pause=0.02, autofmt=False):
        Text.__init__(self, spec, static, pause, autofmt)

    def _parse_spec(self, spec):
        """Overrides the normal Text class behavior. To handle dictation of
        special characters like / . _
        Unfortunately, I have not found a better place to solve this.

        """
        events = []
        try:
            parts = re.split("%\([a-z_0-9]+\)s", self._spec)
            if len(parts) > 2:
                raise Exception("SCText only supports one variable, yet.")
            start = len(parts[0])
            end = len(spec) - len(parts[1])
            words = spec[start:end]
            words = strip_dragon_info(words)
            new_text = ""
            for word in words:
                if (new_text != "" and new_text[-1:].isalnum() and
                        word[-1:].isalnum()):
                    word = " " + word  # Adds spacing between normal words.
                new_text += word
            spec = parts[0] + new_text + parts[1]
            for character in spec:
                if character in self._specials:
                    typeable = self._specials[character]
                else:
                    typeable = Keyboard.get_typeable(character)
                events.extend(typeable.events(self._pause))
        except Exception as e:
            print self._spec, parts
            print("Error: %s" % e)
        return events
