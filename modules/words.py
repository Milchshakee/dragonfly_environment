from dragonfly import Grammar, DictListRef, Config, Section, Item, DictList, Text, List, ListRef, MappingRule

abbreviation_map = DictList("abbreviation_map")
abbreviation_map_reference = DictListRef("abbreviation_map", abbreviation_map)

special_word_map = List("special_word_map")
special_word_map_reference = ListRef("special_word_map", special_word_map)

commands = {
    "abbreviate <abbreviation_map>": Text("%(abbreviation_map)s"),
    "word <special_word_map>": Text("%(special_word_map)s"),
}


def reload_config():
    config = Config("Settings")
    config.words = Section("words")
    config.words.abbreviations = Item({})
    config.words.special_words = Item([])
    config.load()
    global abbreviation_map
    abbreviation_map.update(config.words.abbreviations)
    global special_word_map
    special_word_map.set(config.words.special_words)


def create_grammar():
    grammar = Grammar("words")
    grammar.add_rule(MappingRule(mapping=commands, extras=[
        abbreviation_map_reference,
        special_word_map_reference
    ]))
    return grammar, True
