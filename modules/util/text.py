import re


def extract_dragon_info(input_text):
    new_words = []
    words = str(input_text).split(" ")
    for word in words:
        if word.rfind("\\") > -1:
            pos = word.rfind("\\") + 1
            if (len(word) - 1) >= pos:
                word = word[pos:]  # Remove written form info.
            else:
                word = ""
        new_words.append(word)
    return new_words


special_character_translations = {
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

special_character_translations_regex = re.compile('|'.join(re.escape(key) for key in special_character_translations.keys()))


def strip_dragon_info(text):
    new_words = []
    words = str(text).split(" ")
    for word in words:
        word = special_character_translations_regex.sub(lambda m: special_character_translations[m.group()], word)

        backslash_index = word.find("\\")
        if backslash_index > -1:
            word = word[:backslash_index]  # Remove spoken form info.
        new_words.append(word)
    return new_words
