from dragonfly import *

import modules.util.formatter

DYN_MODULE_NAME = "python"


def define_variable(text):
    modules.util.formatter.snake_case_text(text)
    Text(" = ").execute()


def define_function(text):
    Text("def ").execute()
    modules.util.formatter.snake_case_text(text)
    Text("():").execute()
    Key("left:2").execute()


def define_method(text):
    Text("def ").execute()
    modules.util.formatter.snake_case_text(text)
    Text("(self, ):").execute()
    Key("left:2").execute()


def define_class(text):
    Text("class ").execute()
    modules.util.formatter.pascal_case_text(text)
    Text("():").execute()
    Key("left:2").execute()


rules = MappingRule(
    mapping={
        # Commands and keywords:
        "and": Text(" and "),
        "as": Text("as "),
        "assign": Text(" = "),
        "assert": Text("assert "),
        "break": Text("break"),
        "comment": Text("# "),
        "class": Text("class "),
        "continue": Text("continue"),
        "del": Text("del "),
        "divided by": Text(" / "),
        "enumerate": Text("enumerate()") + Key("left"),
        "(def|define|definition) function <text>": Function(define_function),
        "(def|define|definition) method <text>": Function(define_method),
        "(def|define|definition) init": Text("def __init__("),
        "(def|define|definition) string": Text("\"\"") + Key("left"),
        "[(def|define)] (var|variable) <text> equals": Function(define_variable),
        "(def|define|definition) class <text>": Function(define_class),
        "(var|variable) <text>": Function(modules.util.formatter.snake_case_text),
        "class <text>": Function(modules.util.formatter.pascal_case_text),
        "doc string": Text('"""Doc string."""') + Key("left:14, s-right:11"),
        "else": Text("else:") + Key("enter"),
        "except": Text("except "),
        "exec": Text("exec "),
        "(el if|else if)": Text("elif "),
        "equals": Text(" == "),
        "false": Text("False"),
        "finally": Text("finally:") + Key("enter"),
        "for": Text("for "),
        "from": Text("from "),
        "global ": Text("global "),
        "greater than": Text(" > "),
        "greater [than] equals": Text(" >= "),
        "if": Text("if "),
        "in": Text(" in "),
        "(int|I N T)": Text("int()") + Key("left"),
        "init": Text("init"),
        "import": Text("import "),
        "(len|L E N)": Text("len()") + Key("left"),
        "lambda": Text("lambda "),
        "less than": Text(" < "),
        "less [than] equals": Text(" <= "),
        "(minus|subtract|subtraction)": Text(" - "),
        "(minus|subtract|subtraction) equals": Text(" -= "),
        "modulo": Key("space") + Key("percent") + Key("space"),
        "not": Text(" not "),
        "not equals": Text(" != "),
        "none": Text("None"),
        "or": Text(" or "),
        "pass": Text("pass"),
        "(plus|add|addition)": Text(" + "),
        "(plus|add|addition) equals": Text(" += "),
        "print": Text("print()") + Key("left"),
        "raise": Text("raise"),
        "raise exception": Text("raise Exception()") + Key("left"),
        "return": Text("return "),
        "return nothing": Text("return"),
        "self": Text("self"),
        "(str|S T R)": Text("str()") + Key("left"),
        "true": Text("True"),
        "try": Text("try:") + Key("enter"),
        "times": Text(" * "),
        "with": Text("with "),
        "while": Text("while "),
        "yield": Text("yield "),

        "end (params|parameters)": Key("right:2"),

        # Some common modules.
        "datetime": Text("datetime"),
        "(io|I O)": Text("io"),
        "logging": Text("logging"),
        "(os|O S)": Text("os"),
        "(pdb|P D B)": Text("pdb"),
        "(re|R E)": Text("re"),
        "(sys|S Y S)": Text("sys"),
        "S Q lite 3": Text("sqlite3"),
        "subprocess": Text("subprocess"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)


def create_grammar():
    grammar = Grammar("Python grammar")
    grammar.add_rule(rules)
    return grammar, False
