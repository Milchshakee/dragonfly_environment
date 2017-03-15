import time
import win32api, win32con, win32gui
from dragonfly import (Grammar, Alternative, RuleRef, DictListRef,
                       Dictation, Compound, Rule, CompoundRule,
                       DictList, Window, Rectangle, monitors,
                       Config, Section, Item, FocusWindow, ActionError)


grammar = Grammar("window control")

config = Config("Settings")
config.settings = Section("Settings")
config.settings.commands = Item({})
config.load()


executable_names = DictList("executable_names", config.settings.commands)
executable_names_ref = DictListRef("executable_names", executable_names)

current_executable = None
available_configurations = DictList("available_configurations")
available_configurations_reference = DictListRef("available_configurations", available_configurations)
current_configuration = None
current_parameter = None


class CommandRule(CompoundRule):

    spec = "command <executable_names>"
    extras = [executable_names_ref]

    def _process_recognition(self, node, extras):
        global current_executable
        global available_configurations
        if current_executable is None:
            current_executable = config.settings.commands[extras["executable_names"]]["path"]
            available_configurations = config.settings.commands[extras["executable_names"]]["configurations"]

grammar.add_rule(CommandRule())


class ConfigRule(CompoundRule):

    spec = "config <available_configurations>"
    extras = [available_configurations_reference]

    def _process_recognition(self, node, extras):
        global current_configuration
        current_configuration = available_configurations[]

grammar.add_rule(ConfigRule())


grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
