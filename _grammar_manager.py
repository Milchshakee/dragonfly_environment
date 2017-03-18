import sys
import pkgutil

from dragonfly import (
    MappingRule,
    Function,
    Choice,
    Grammar
)

import grammars

active_module = None
module_mapping = {}


def enable_module(module):
    global active_module
    if active_module is not None:
        return
    module.dynamic_enable()
    active_module = module


def disable_active_module():
    global active_module
    if active_module is None:
        return
    active_module.dynamic_disable()
    active_module = None


def import_dynamic_modules():
    global module_mapping
    path = grammars.__path__
    prefix = grammars.__name__ + "."
    print("Loading dynamic grammar modules:")
    for importer, package_name, _ in pkgutil.iter_modules(path, prefix):
        if package_name not in sys.modules:
            try:
                module = importer.find_module(package_name).load_module(package_name)
            except Exception, cause:
                print("Could not load %s:" % package_name)
                print(cause)
            else:
                module_mapping[module.DYN_MODULE_NAME] = module
                print("Loaded %s" % package_name)


import_dynamic_modules()

commands = MappingRule(
    mapping={
        "enable <module> mode": Function(enable_module),
        "disable current mode": Function(disable_active_module)
    },
    extras=[
        Choice("module", module_mapping)
    ]
)

grammar = Grammar("Dynamic manager")
grammar.add_rule(commands)
grammar.load()


def unload():
    global module_mapping
    for module in module_mapping.values():
        module.unload()

    global grammar
    if grammar:
        grammar.unload()
    grammar = None
