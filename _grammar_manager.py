"""A command module for Dragonfly, for dynamically enabling/disabling
different grammars.

If a grammar is enabled that is conflicting with a previously enabled grammar,
the previously enabled grammar will be automatically disabled.
Each dynamic grammar module is responsible for keeping track of what other
modules it is incompatible with.

-----------------------------------------------------------------------------
Licensed under LGPL3

"""
import sys
import pkgutil

from dragonfly import (
    CompoundRule,
    MappingRule,
    RuleRef,
    Repetition,
    Function,
    IntegerRef,
    Dictation,
    Choice,
    Grammar
)

import grammar_config

config = grammar_config.get_config()

import grammars

moduleMapping = {}


def enable_module(module, useSound=True):
    """Enables the specified module. Disables conflicting modules."""
    if not module:
        return
    moduleName = module.DYN_MODULE_NAME
    disable_incompatible_modules(module)
    status = module.dynamic_enable()
    if status:
        grammar_config.get_config()[moduleName] = True
        grammar_config.save_config()


def disable_module(module, useSound=True):
    """Disabled the specified module."""
    if not module:
        return
    status = module.dynamic_disable()
    moduleName = module.DYN_MODULE_NAME
    if status:
        config = grammar_config.get_config()
        config[moduleName] = False
        grammar_config.save_config()


def disable_incompatible_modules(enableModule):
    """Iterates through the list of incompatible modules and disables them."""
    global moduleMapping
    for moduleName in enableModule.INCOMPATIBLE_MODULES:
        module = moduleMapping.get(moduleName)
        if module:
            disable_module(module, useSound=True)


def import_dynamic_modules():
    global moduleMapping
    config = grammar_config.get_config()
    path = grammars.__path__
    prefix = grammars.__name__ + "."
    print("Loading dynamic grammar modules:")
    for importer, package_name, _ in pkgutil.iter_modules(path, prefix):
        if package_name not in sys.modules:
            module = importer.find_module(package_name).load_module(
                package_name)
            moduleMapping[module.DYN_MODULE_NAME] = module
            enabled = config.get(module.DYN_MODULE_NAME, False)
            print("    %s" % package_name)
            if enabled == True:
                enable_module(module, useSound=False)


import_dynamic_modules()


def disable_all_modules(useSound=True):
    """Iterates through the list of all dynamic modules and disables them."""
    global moduleMapping
    disableCount = 0
    config = grammar_config.get_config()
    for moduleName, module in moduleMapping.items():
        status = module.dynamic_disable()
        if status:
            disableCount += 1
            config[moduleName] = False
    if disableCount > 0:
        grammar_config.save_config()
        print("----------- All dynamic modules disabled -----------\n")
    else:
        print("---------- No dynamic modules are enabled ----------\n")


def enable_modules(module, module2=None, module3=None, disableOthers=False):
    if disableOthers:
        disable_all_modules(useSound=False)
    modules = [module, module2, module3]
    incompatibleModules = []
    for module in modules:
        if module:
            if not module.DYN_MODULE_NAME in incompatibleModules:
                enable_module(module)
                incompatibleModules.extend(module.INCOMPATIBLE_MODULES)
            else:
                print("Grammar %s is incompatible with previous grammar" %
                    module.DYN_MODULE_NAME)

class SeriesMappingRule(CompoundRule):
    def __init__(self, mapping, extras=None, defaults=None):
        mapping_rule = MappingRule(mapping=mapping, extras=extras,
            defaults=defaults, exported=False)
        single = RuleRef(rule=mapping_rule)
        series = Repetition(single, min=1, max=16, name="series")

        compound_spec = "<series>"
        compound_extras = [series]
        CompoundRule.__init__(self, spec=compound_spec,
            extras=compound_extras, exported=True)

    def _process_recognition(self, node, extras):  # @UnusedVariable
        series = extras["series"]
        for action in series:
            action.execute()

series_rule = SeriesMappingRule(
    mapping={
        "enable <module> mode": Function(enable_modules),
        "enable <module> mode only": Function(enable_modules, disableOthers=True),  # @IgnorePep8
        "enable <module> and <module2> mode": Function(enable_modules),  # @IgnorePep8
        "enable <module> and <module2> mode only": Function(enable_modules, disableOthers=True),  # @IgnorePep8
        "enable <module> and <module2> and <module3> mode": Function(enable_modules),  # @IgnorePep8
        "enable <module> and <module2> and <module3> mode only": Function(enable_modules, disableOthers=True),  # @IgnorePep8
        "disable <module> mode": Function(disable_module),
        "disable [all] dynamic modes": Function(disable_all_modules),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("module", moduleMapping),
        Choice("module2", moduleMapping),
        Choice("module3", moduleMapping),
    ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Dynamic manager", context=None)
grammar.add_rule(series_rule)
grammar.load()


def unload():
    global moduleMapping
    for module in moduleMapping.values():
        module.unload()

    global grammar
    if grammar:
        grammar.unload()
    grammar = None
