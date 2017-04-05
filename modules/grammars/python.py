from dragonfly import *

import modules.util.formatter as formatter
import modules.global_state as global_state
from modules.util.dragonfly_utils import PositionalText, SurroundRule


class DefineClassRule(CompoundRule):

    spec = "(def|define) [child] class [<text>] "
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        is_child = node.words()[1] == "child"
        string = "class "
        if "text" in extras:
            string += formatter.format_text(extras["text"], formatter.FormatType.pascalCase)

        if is_child:
            string += "()"
        PositionalText(string).execute()
        if is_child:
            global_state.add_nesting_level(1)
            if "text" not in extras:
                global_state.add_nesting_level(1)


class DefineVariableRule(CompoundRule):

    spec = "(def|define) (variable|constant) [<text>] [equals]"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        type = node.words()[1]
        string = ""
        if "text" in extras:
            if type == "variable":
                name = formatter.format_snake_case(extras["text"])
            else:
                name = formatter.format_text(extras["text"], [formatter.FormatType.snakeCase, formatter.FormatType.upperCase])

            string = name

        string += " = "
        PositionalText(string).execute()
        if "text" not in extras:
            global_state.add_nesting_level(3)


class DefineFunctionRule(CompoundRule):

    spec = "(def|define) [no-param] (constructor | ((function | method) [<text>]))"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        has_parameters = node.words()[1] != "no-param"
        type = node.words()[1 if has_parameters else 2]
        string = "def "

        name = None
        if type == "constructor":
            name = "__init__"
        elif "text" in extras:
            name = formatter.format_snake_case(extras["text"])

        if name is not None:
            string += name

        parameters_start = "("
        if type in ("method", "constructor"):
            parameters_start += "self, " if has_parameters else "self"

        string += parameters_start + ")"
        PositionalText(string).execute()
        if has_parameters:
            global_state.add_nesting_level(1)
        if name is None:
            name_offset = len(parameters_start)
            if not has_parameters:
                name_offset += 1
            global_state.add_nesting_level(name_offset)


class CallFunctionRule(CompoundRule):

    spec = "call [empty] (constructor | function <text>) [on]"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        is_constructor = "text" not in extras
        name = "__init__" if is_constructor else formatter.format_text(extras["text"], formatter.FormatType.snakeCase)
        has_arguments = node.words()[1] != "empty"
        has_period = node.words()[len(node.words()) - 1] == "on"
        string = "." if has_period else ""
        string += name
        string += "()"
        PositionalText(string).execute()

        if has_arguments:
            global_state.add_nesting_level(1)


class CreateObjectRule(CompoundRule):

    spec = "create [empty] <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        has_arguments = node.words()[1] != "empty"
        string = formatter.format_text(extras["text"], formatter.FormatType.pascalCase)
        string += "()"
        PositionalText(string).execute()

        if has_arguments:
            global_state.add_nesting_level(1)


def ternary():
    PositionalText(" if  else ").execute()
    global_state.add_nesting_level(6)
    global_state.add_nesting_level(4)


def list_comprehension():
    PositionalText("[ for  in ]").execute()
    global_state.add_nesting_level(1)
    global_state.add_nesting_level(4)
    global_state.add_nesting_level(5)


def format_variable(text, prefix="", suffix=""):
    name = formatter.format_text(text, formatter.FormatType.snakeCase)
    PositionalText(prefix + name + suffix).execute()


def class_name(text):
    name = formatter.format_text(text, formatter.FormatType.pascalCase)
    PositionalText(name).execute()

rules = MappingRule(
    mapping={
        # Commands and keywords:
        "and": PositionalText(" and "),
        "as": PositionalText("as "),
        "assign": PositionalText(" = "),
        "assert": PositionalText("assert "),
        "break": PositionalText("break"),
        "comment": PositionalText("# "),
        "class": PositionalText("class "),
        "continue": PositionalText("continue"),
        "del": PositionalText("del "),
        "divided by": PositionalText(" / "),
        "string <text>": PositionalText("\"%(text)s\""),
        "(var|variable) <text>": Function(format_variable),
        "(arg|argument) <text>": Function(format_variable, suffix="="),
        "private": PositionalText("__"),
        "private <text>": Function(format_variable, prefix="__"),
        "protected": PositionalText("_"),
        "protected <text>": Function(format_variable, prefix="_"),
        "class <text>": Function(class_name),
        "else": PositionalText("else:") + Key("enter"),
        "except": PositionalText("except "),
        "exec": PositionalText("exec "),
        "(el if|else if)": PositionalText("elif "),
        "equals": PositionalText(" == "),
        "false": PositionalText("False"),
        "finally": PositionalText("finally:\n"),
        "for": PositionalText("for "),
        "from": PositionalText("from "),
        "global ": PositionalText("global "),
        "global <text>": Function(format_variable, prefix="global "),
        "greater than": PositionalText(" > "),
        "greater [than] equals": PositionalText(" >= "),
        "if": PositionalText("if "),
        "if not": PositionalText("if not "),
        "in": PositionalText(" in "),
        "is": PositionalText(" is "),
        "is not": PositionalText(" is not "),
        "import": PositionalText("import "),
        "lambda": PositionalText("lambda "),
        "less than": PositionalText(" < "),
        "less [than] equals": PositionalText(" <= "),
        "list comprehension": Function(list_comprehension),
        "(minus|subtract|subtraction)": PositionalText(" - "),
        "(minus|subtract|subtraction) equals": PositionalText(" -= "),
        "modulo": PositionalText(" % "),
        "not": PositionalText(" not "),
        "not equals": PositionalText(" != "),
        "none": PositionalText("None"),
        "or": PositionalText(" or "),
        "pass": PositionalText("pass"),
        "(plus|add|addition)": PositionalText(" + "),
        "(plus|add|addition) equals": PositionalText(" += "),
        "raise": PositionalText("raise "),
        "return": PositionalText("return "),
        "return nothing": PositionalText("return"),
        "self": PositionalText("self"),
        "ternary": Function(ternary),
        "true": PositionalText("True"),
        "try": PositionalText("try:\n"),
        "times": PositionalText(" * "),
        "with": PositionalText("with "),
        "while": PositionalText("while "),
        "yield": PositionalText("yield "),

        "start block": Function(global_state.clear_nesting_levels) + Key("end") + PositionalText(":\n"),
        "new entry": Function(global_state.clear_nesting_levels) + Key("end") + PositionalText(",\n"),
        "next [(arg|argument)]": Function(global_state.remove_nesting_levels) + PositionalText(", "),
        "value": Function(global_state.remove_nesting_levels) + PositionalText(": "),

        # Some common modules.
        "datetime": PositionalText("datetime"),
        "(io|I O)": PositionalText("io"),
        "logging": PositionalText("logging"),
        "(os|O S)": PositionalText("os"),
        "(pdb|P D B)": PositionalText("pdb"),
        "(re|R E)": PositionalText("re"),
        "(sys|S Y S)": PositionalText("sys"),
        "S Q lite 3": PositionalText("sqlite3"),
        "subprocess": PositionalText("subprocess"),
    },
    extras=[
        Dictation("text"),
    ]
)


def create_grammar():
    grammar = Grammar("python")
    grammar.add_rule(rules)
    grammar.add_rule(DefineFunctionRule())
    grammar.add_rule(DefineVariableRule())
    grammar.add_rule(CallFunctionRule())
    grammar.add_rule(CreateObjectRule())
    grammar.add_rule(SurroundRule("string", "\"", "\""))
    grammar.add_rule(SurroundRule("to string", "str(", ")"))
    grammar.add_rule(SurroundRule("list", "list(", ")"))
    grammar.add_rule(SurroundRule("dictionary", "dict(", ")"))
    grammar.add_rule(SurroundRule("int", "int(", ")"))
    grammar.add_rule(SurroundRule("length", "len(", ")"))
    grammar.add_rule(SurroundRule("print", "print(", ")"))
    grammar.add_rule(SurroundRule("doc string", '"""', '"""'))
    global_state.add_dictation_incompatible_grammar(grammar)
    return grammar, False
