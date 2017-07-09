from dragonfly import *

mapping = {
    "go back [<n>]": Key("a-left/15:%(n)d"),
    "go forward [<n>]": Key("a-right/15:%(n)d"),
    "[open] new window": Key("c-n"),
    "close window": Key("cs-w"),
    "undo close window": Key("cs-n"),
    "[open] new tab": Key("c-t"),
    "close tab": Key("c-w"),
    "close <n> tabs": Key("c-w/20:%(n)d"),
    "[go to] next tab [<n>]": Key("c-tab:%(n)d"),
    "[go to] previous tab [<n>]": Key("cs-tab:%(n)d"),
    "(restore|undo close) tab": Key("cs-t"),
    "go to search [bar]": Key("c-k"),
    "go to address [bar]": Key("a-d"),
    "copy address": Key("a-d/10, c-c/10"),
    "paste address": Key("a-d/10, c-v/10"),
    "go home": Key("a-home"),
    "stop loading": Key("escape"),
    "reload [page]": Key("f5"),
    "bookmarks": Key("cs-b"),

    "bookmark [this] page": Key("c-d"),
    "find in page": Key("c-f"),
    "close find": Key("escape"),
    "find previous [<n>]": Key("s-f3/10:%(n)d"),
    "find next [<n>]": Key("f3/10:%(n)d"),

    "go to tab [<n>]": Key("c-%(n)d") + Key("a-%(n)d")
}


def create_grammar():
    firefox_context = AppContext(executable="firefox")
    grammar = Grammar("firefox", context=firefox_context)
    grammar.add_rule(MappingRule(mapping=mapping, extras=[IntegerRef("n", 1, 9)], defaults={"n": 1}))
    return grammar, True
