import re

from dragonfly import *

import text


class FormatTypes:
    camelCase = 1
    pascalCase = 2
    snakeCase = 3
    squash = 4
    upperCase = 5
    lowerCase = 6
    dashify = 7
    dotify = 8
    spokenForm = 9


def format_camel_case(input_text):
    new_text = ""
    words = text.strip_dragon_info(input_text)
    for word in words:
        if new_text == '':
            new_text = word[:1].lower() + word[1:]
        else:
            new_text = '%s%s' % (new_text, word.capitalize())
    return new_text


def format_pascal_case(input_text):
    new_text = ""
    words = text.strip_dragon_info(input_text)
    for word in words:
        new_text = '%s%s' % (new_text, word.capitalize())
    return new_text


def format_snake_case(input_text):
    new_text = ""
    words = text.strip_dragon_info(input_text)
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            word = "_" + word  # Adds underscores between normal words.
        new_text += word.lower()
    return new_text


def format_dashify(input_text):
    new_text = ""
    words = text.strip_dragon_info(input_text)
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            word = "-" + word  # Adds dashes between normal words.
        new_text += word
    return new_text


def format_dotify(input_text):
    new_text = ""
    words = text.strip_dragon_info(input_text)
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            word = "." + word  # Adds dashes between normal words.
        new_text += word
    return new_text


def format_squash(input_text):
    new_text = ""
    words = text.strip_dragon_info(input_text)
    for word in words:
        new_text = '%s%s' % (new_text, word)
    return new_text


def format_upper_case(input_text):
    new_text = ""
    words = text.strip_dragon_info(input_text)
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            word = " " + word  # Adds spacing between normal words.
        new_text += word.upper()
    return new_text


def format_lower_case(input_text):
    new_text = ""
    words = text.strip_dragon_info(input_text)
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            if new_text[-1:] != "." and word[0:1] != ".":
                word = " " + word  # Adds spacing between normal words.
        new_text += word.lower()
    return new_text


def format_spoken_form(input_text):
    new_text = ""
    words = text.extract_dragon_info(input_text)
    for word in words:
        if new_text != "":
            word = " " + word
        new_text += word
    return new_text


FORMAT_TYPES_MAP = {
    FormatTypes.camelCase: format_camel_case,
    FormatTypes.pascalCase: format_pascal_case,
    FormatTypes.snakeCase: format_snake_case,
    FormatTypes.squash: format_squash,
    FormatTypes.upperCase: format_upper_case,
    FormatTypes.lowerCase: format_lower_case,
    FormatTypes.dashify: format_dashify,
    FormatTypes.dotify: format_dotify,
    FormatTypes.spokenForm: format_spoken_form,
}


def format_text(text, format_type):
    if format_type:
        if type(format_type) != type([]):
            format_type = [format_type]
        result = ""
        for value in format_type:
            if not result:
                if format_type == FormatTypes.spokenForm:
                    result = text.words
                else:
                    result = str(text)
            method = FORMAT_TYPES_MAP[value]
            result = method(result)
        Text("%(text)s").execute({"text": result})


def camel_case_text(input_text):
    """Formats dictated text to camel case.

    Example:
    "'camel case my new variable'" => "myNewVariable".

    """
    new_text = format_camel_case(input_text)
    Text("%(text)s").execute({"text": new_text})


def camel_case_count(n):
    """Formats n words to the left of the cursor to camel case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'camel case 3'" => "myNewVariable".

    """
    save_text = _get_clipboard_text()
    cut_text = _select_and_cut_text(n)
    if cut_text:
        end_space = cut_text.endswith(' ')
        text = _cleanup_text(cut_text)
        new_text = _camelify(text.split(' '))
        if end_space:
            new_text = new_text + ' '
        new_text = new_text.replace("%", "%%")  # Escape any format chars.
        Text(new_text).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(save_text)


def _camelify(words):
    """Takes a list of words and returns a string formatted to camel case.

    Example:
    ["my", "new", "variable"] => "myNewVariable".

    """
    new_text = ''
    for word in words:
        if new_text == '':
            new_text = word[:1].lower() + word[1:]
        else:
            new_text = '%s%s' % (new_text, word.capitalize())
    return new_text


def pascal_case_text(text):
    """Formats dictated text to pascal case.

    Example:
    "'pascal case my new variable'" => "MyNewVariable".

    """
    new_text = format_pascal_case(text)
    Text("%(text)s").execute({"text": new_text})


def pascal_case_count(n):
    """Formats n words to the left of the cursor to pascal case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'pascal case 3'" => "MyNewVariable".

    """
    save_text = _get_clipboard_text()
    cut_text = _select_and_cut_text(n)
    if cut_text:
        end_space = cut_text.endswith(' ')
        text = _cleanup_text(cut_text)
        new_text = text.title().replace(' ', '')
        if end_space:
            new_text += ' '
        new_text = new_text.replace("%", "%%")  # Escape any format chars.
        Text(new_text).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(save_text)


def snake_case_text(text):
    """Formats dictated text to snake case.

    Example:
    "'snake case my new variable'" => "my_new_variable".

    """
    new_text = format_snake_case(text)
    Text("%(text)s").execute({"text": new_text})


def snake_case_count(n):
    """Formats n words to the left of the cursor to snake case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'snake case 3'" => "my_new_variable".

    """
    save_text = _get_clipboard_text()
    cut_text = _select_and_cut_text(n)
    if cut_text:
        end_space = cut_text.endswith(' ')
        text = _cleanup_text(cut_text.lower())
        new_text = '_'.join(text.split(' '))
        if end_space:
            new_text = new_text + ' '
        new_text = new_text.replace("%", "%%")  # Escape any format chars.
        Text(new_text).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(save_text)


def squash_text(text):
    """Formats dictated text with whitespace removed.

    Example:
    "'squash my new variable'" => "mynewvariable".

    """
    new_text = format_squash(text)
    Text("%(text)s").execute({"text": new_text})


def squash_count(n):
    """Formats n words to the left of the cursor with whitespace removed.
    Excepting spaces immediately after comma, colon and percent chars.

    Note: Word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'squash 3'" => "mynewvariable".
    "'my<tab>new variable' *pause* 'squash 3'" => "mynewvariable".
    "( foo = bar, fee = fye )", 'squash 9'" => "(foo=bar, fee=fye)"

    """
    save_text = _get_clipboard_text()
    cut_text = _select_and_cut_text(n)
    if cut_text:
        end_space = cut_text.endswith(' ')
        text = _cleanup_text(cut_text)
        new_text = ''.join(text.split(' '))
        if end_space:
            new_text = new_text + ' '
        new_text = _expand_after_special_chars(new_text)
        new_text = new_text.replace("%", "%%")  # Escape any format chars.
        Text(new_text).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(save_text)


def expand_count(n):
    """Formats n words to the left of the cursor by adding whitespace in
    certain positions.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example, with to compact code:
    "result=(width1+width2)/2 'expand 9' " => "result = (width1 + width2) / 2"

    """
    save_text = _get_clipboard_text()
    cut_text = _select_and_cut_text(n)
    if cut_text:
        end_space = cut_text.endswith(' ')
        cut_text = _expand_after_special_chars(cut_text)
        reg = re.compile(
            r'([a-zA-Z0-9_\"\'\)][=\+\-\*/\%]|[=\+\-\*/\%][a-zA-Z0-9_\"\'\(])')
        hit = reg.search(cut_text)
        count = 0
        while hit and count < 10:
            cut_text = cut_text[:hit.start() + 1] + ' ' + \
                cut_text[hit.end() - 1:]
            hit = reg.search(cut_text)
            count += 1
        new_text = cut_text
        if end_space:
            new_text += ' '
        new_text = new_text.replace("%", "%%")  # Escape any format chars.
        Text(new_text).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(save_text)


def _expand_after_special_chars(text):
    reg = re.compile(r'[:,%][a-zA-Z0-9_\"\']')
    hit = reg.search(text)
    count = 0
    while hit and count < 10:
        text = text[:hit.start() + 1] + ' ' + text[hit.end() - 1:]
        hit = reg.search(text)
        count += 1
    return text


def uppercase_text(text):
    """Formats dictated text to upper case.

    Example:
    "'upper case my new variable'" => "MY NEW VARIABLE".

    """
    new_text = format_upper_case(text)
    Text("%(text)s").execute({"text": new_text})


def uppercase_count(n):
    """Formats n words to the left of the cursor to upper case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'upper case 3'" => "MY NEW VARIABLE".

    """
    save_text = _get_clipboard_text()
    cut_text = _select_and_cut_text(n)
    if cut_text:
        new_text = cut_text.upper()
        new_text = new_text.replace("%", "%%")  # Escape any format chars.
        Text(new_text).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(save_text)


def lowercase_text(text):
    """Formats dictated text to lower case.

    Example:
    "'lower case John Johnson'" => "john johnson".

    """
    new_text = format_lower_case(text)
    Text("%(text)s").execute({"text": new_text})


def lowercase_count(n):
    """Formats n words to the left of the cursor to lower case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'John Johnson' *pause* 'lower case 2'" => "john johnson".

    """
    save_text = _get_clipboard_text()
    cut_text = _select_and_cut_text(n)
    if cut_text:
        new_text = cut_text.lower()
        new_text = new_text.replace("%", "%%")  # Escape any format chars.
        Text(new_text).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(save_text)


def _cleanup_text(input_text):
    """Cleans up the text before formatting to camel, pascal or snake case.

    Removes dashes, underscores, single quotes (apostrophes) and replaces
    them with a space character. Multiple spaces, tabs or new line characters
    are collapsed to one space character.
    Returns the result as a string.

    """
    prefixChars = ""
    suffixChars = ""
    if input_text.startswith("-"):
        prefixChars += "-"
    if input_text.startswith("_"):
        prefixChars += "_"
    if input_text.endswith("-"):
        suffixChars += "-"
    if input_text.endswith("_"):
        suffixChars += "_"
    input_text = input_text.strip()
    input_text = input_text.replace('-', ' ')
    input_text = input_text.replace('_', ' ')
    input_text = input_text.replace("'", ' ')
    input_text = re.sub('[ \t\r\n]+', ' ', input_text)  # Any whitespaces to one space.
    input_text = prefixChars + input_text + suffixChars
    return input_text


def _get_clipboard_text():
    """Returns the text contents of the system clip board."""
    clipboard = Clipboard()
    return clipboard.get_system_text()


def _select_and_cut_text(wordCount):
    """Selects wordCount number of words to the left of the cursor and cuts
    them out of the text. Returns the text from the system clip board.

    """
    clipboard = Clipboard()
    clipboard.set_system_text('')
    Key('cs-left/3:%s/10, c-x/10' % wordCount).execute()
    return clipboard.get_system_text()


def _set_clipboard_text(text):
    """Sets the system clip board content."""
    clipboard = Clipboard()
    clipboard.set_text(text)  # Restore previous clipboard text.
    clipboard.copy_to_system()
