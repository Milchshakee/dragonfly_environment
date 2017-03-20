import sys
import os
import pkgutil
import imp
from dragonfly import *

loaded_modules = {}

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


def load_package(path):
    absolute_path = os.path.join(ROOT_PATH, path)
    package_name = os.path.basename(path)
    package_dotted_name = os.path.normpath(path).replace(os.path.sep, ".")
    package_tuple = imp.find_module(package_name, [os.path.dirname(absolute_path)])
    package = imp.load_module(package_dotted_name, *package_tuple)

    loaded_modules[package] = None
    print("Loaded package %s" % package_dotted_name)

    prefix = package_dotted_name + "."
    for importer, module_name, _ in pkgutil.iter_modules([package_tuple[1]], prefix):
        if module_name in sys.modules:
            module = sys.modules[module_name]
            print("Module %s already loaded" % module_name)
        else:
            try:
                module = importer.find_module(module_name).load_module(module_name)
            except Exception, cause:
                print("Could not load %s:" % module_name)
                print(cause)
                continue
            else:
                print("Loaded module %s" % module_name)

        loaded_modules[module] = None

    directories = [f for f in os.listdir(absolute_path) if os.path.isdir(os.path.join(absolute_path, f))]
    for directory in directories:
        load_package(os.path.join(path, directory))


def load_modules():
    print("Loading modules:")
    load_package("modules")

    for module in loaded_modules.keys():
        if "create_grammar" in module.__dict__:
            loaded_grammar = module.create_grammar()
            loaded_grammar[0].load()
            if not loaded_grammar[1]:
                loaded_grammar[0].disable()
            loaded_modules[module] = loaded_grammar[0]
        if "load" in module.__dict__:
            module.load()
        if "load_config" in module.__dict__:
            module.load_config()


def unload_modules():
    for module in loaded_modules.keys():
        if "unload" in module.__dict__:
            module.unload()

        module_grammar = loaded_modules[module]
        if module_grammar is not None:
            module_grammar.unload()

    for module in loaded_modules.copy().keys():
        del loaded_modules[module]
        del sys.modules[module.__name__]
        del module


def enable_grammar(g):
    if g.enabled:
        print("Grammar %s is already enabled" % g.name)
    else:
        g.enable()
        print("Grammar %s enabled" % g.name)


def disable_grammar(g):
    if not g.enabled:
        print("Grammar %s is not enabled" % g.name)
    else:
        g.disable()
        print("Grammar %s disabled" % g.name)


def reload_configurations():
    for module in loaded_modules.keys():
        if "reload_config" in module.__dict__:
            module.reload_config()
    print("Reloaded configurations")


load_modules()

commands = MappingRule(
    mapping={
        "reload modules": Function(unload_modules) + Function(load_modules),
        "enable <g> grammar": Function(enable_grammar),
        "disable <g> grammar": Function(disable_grammar),
        "reload configurations": Function(reload_configurations)

    },
    extras=[Choice("g", dict((g.name, g) for g in filter(lambda g: g is not None, loaded_modules.values())))]
)

grammar = Grammar("Dynamic manager")
grammar.add_rule(commands)
grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

    unload_modules()
