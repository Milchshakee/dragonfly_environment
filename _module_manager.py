import sys
import os
import pkgutil
import imp
import traceback
from dragonfly import *

loaded_modules = []
loaded_grammars = DictList("g")
loaded_grammars_ref = DictListRef("g", loaded_grammars)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


def load_package(path):
    absolute_path = os.path.join(ROOT_PATH, path)
    package_name = os.path.basename(path)
    package_dotted_name = os.path.normpath(path).replace(os.path.sep, ".")
    package_tuple = imp.find_module(package_name, [os.path.dirname(absolute_path)])
    package = imp.load_module(package_dotted_name, *package_tuple)

    loaded_modules.append(package)
    print(" - pkg %s" % package_dotted_name)

    prefix = package_dotted_name + "."
    for importer, module_name, ispkg in pkgutil.iter_modules([package_tuple[1]], prefix):
        if ispkg:
            continue

        if module_name in sys.modules:
            module = sys.modules[module_name]
            print(" - (%s)" % module_name)
        else:
            try:
                module = importer.find_module(module_name).load_module(module_name)
            except:
                print("Could not load %s:" % module_name)
                print(traceback.format_exc())
                continue
            else:
                print(" - %s" % module_name)

        loaded_modules.append(module)

    directories = [f for f in os.listdir(absolute_path) if os.path.isdir(os.path.join(absolute_path, f))]
    for directory in directories:
        load_package(os.path.join(path, directory))


def load_modules():
    print("\nLoading modules:")
    load_package("modules")

    print("\nInitializing modules:")
    for module in loaded_modules:
        if "load" in module.__dict__:
            try:
                module.load()
                print(" - %s" % module.__name__)
            except:
                print("Could not initialize %s:" % module.__name__)
                print(traceback.format_exc())
                continue


def load_grammars():
    print("\nLoading grammars:")
    for module in loaded_modules:
        if "create_grammar" in module.__dict__:
            try:
                loaded_grammar, enabled = module.create_grammar()
            except:
                print("Could not load grammar of %s:" % module.__name__)
                print(traceback.format_exc())
                continue
            loaded_grammar.load()
            if not enabled:
                loaded_grammar.disable()
            loaded_grammars[loaded_grammar.name] = loaded_grammar
            print(" - %s" % loaded_grammar.name)


def unload_modules():
    print("\nUnloading modules:")
    for module in list(loaded_modules):
        try:
            if "unload" in module.__dict__:
                module.unload()
        except:
            print("Could not unload %s:" % module.__name__)
            print(traceback.format_exc())
            continue
        loaded_modules.remove(module)
        del sys.modules[module.__name__]
        print(" - %s" % module.__name__)
        del module


def unload_grammars():
    for g in loaded_grammars.values():
        g.unload()
    loaded_grammars.clear()


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
    print("\nLoading configurations:")
    for module in loaded_modules:
        if "reload_config" in module.__dict__:
            module.reload_config()
            print(" - %s" % module.__name__)


load_modules()
reload_configurations()
load_grammars()

commands = MappingRule(
    mapping={
        "reload modules": Function(unload_modules) + Function(load_modules),
        "enable <g> grammar": Function(enable_grammar),
        "disable <g> grammar": Function(disable_grammar),
        "reload configurations": Function(reload_configurations)

    },
    extras=[loaded_grammars_ref]
)

grammar = Grammar("Dynamic manager")
grammar.add_rule(commands)
grammar.load()


def unload():
    unload_grammars()
    unload_modules()

    global grammar
    if grammar:
        grammar.unload()
    grammar = None
