from dragonfly import *

mapping = {
    "(play|pause)": Key("space"),
    "faster": Key("plus"),
    "slower": Key("minus"),

    "assign <n>": Key("control:down/3, %(n)d/3, control:up/3"),
    "army <n>": Key("%(n)d"),

    "court": Key("1"),
    "government": Key("2"),
    "diplomacy": Key("3"),
    "economy": Key("4"),
    "trade": Key("5"),
    "technology": Key("6"),
    "ideas": Key("f1/3, 7"),
    "missions": Key("8"),
    "expansion": Key("9"),
    "religion": Key("0"),
    "military": Key("f2"),
    "subjects": Key("f3"),
    "estates": Key("f4"),

    "court menu": Key("f1/3, 1"),
    "government menu": Key("f1/3, 2"),
    "diplomacy menu": Key("f1/3, 3"),
    "economy menu": Key("f1/3, 4"),
    "trade menu": Key("f1/3, 5"),
    "technology menu": Key("f1/3, 6"),
    "ideas menu": Key("f1/3, 7"),
    "missions menu": Key("f1/3, 8"),
    "expansion menu": Key("f1/3, 9"),
    "religion menu": Key("f1/3, 0"),
    "military menu": Key("f1/3, f2"),
    "subjects menu": Key("f1/3, f3"),
    "estates menu": Key("f1/3, f4"),

    "attach": Key("a"),
    "split": Key("s"),
    "create unit": Key("b"),
    "split": Key("s"),
    "stack": Key("b/3, b/3, c/3"),
    "detach siege": Key("d"),
    "merge units": Key("g"),
    "siege view": Key("j"),
    "consolidate": Key("k"),
    "forced march": Key("m"),
    "detach mercenaries": Key("n"),
    "detach infantry": Key("z"),
    "detach cavalry": Key("x"),
    "detach artillery": Key("c"),
    "(detach transports|build units)": Key("v"),

    "find province": Key("f"),
    "empire": Key("h"),
    "papacy": Key("c"),
    "ledger": Key("l"),
    "close": Key("escape"),
    "accept": Key("enter"),

    "land units": Key("1"),
    "naval units": Key("2"),
    "cores": Key("3"),
    "missionaries": Key("4"),
    "autonomy": Key("5"),
    "cultures": Key("6"),
    "buildings": Key("7"),
    "development": Key("8"),
    "estate land": Key("9"),

    "land units menu": Key("b, 1"),
    "naval units menu": Key("b, 2"),
    "cores menu": Key("b, 3"),
    "missionaries menu": Key("b, 4"),
    "autonomy menu": Key("b, 5"),
    "cultures menu": Key("b, 6"),
    "buildings menu": Key("b, 7"),
    "development menu": Key("b, 8"),
    "estate land menu": Key("b, 9"),

    "move": Mouse("right"),
    "country": Mouse("right"),
    "diplomacy": Key("a"),
    "opinion": Key("s"),
    "feedback": Key("d"),
    "province": Mouse("left"),


}


def create_grammar():
    eu4_context = AppContext(executable="eu4")
    grammar = Grammar("eu4", context=eu4_context)
    grammar.add_rule(MappingRule(mapping=mapping, extras=[IntegerRef("n", 1, 9)]))
    return grammar, True
