from modules.util.utils import shell_context, normal_context
from dragonfly import *

shortcuts = {}

existing_path = False
current_path = None
current_drive = None
current_components = []

def change_drive(drive):
    global current_drive
    current_drive = drive + ":\\"

def append_component(component):
    current_components.append(component)


class PathRule(CompoundRule):

    spec = "[existing] path [from <shortcut>]"
    extras = [Choice("shortcut", shortcuts)]

    def _process_recognition(self, node, extras):
        if "existing" in node.words():
            global existing_path
            existing_path = True
        if "shortcut" in extras:
            global current_path
            current_path = extras["shortcut"]

class PathRule(CompoundRule):
    spec = "directory <directory>"

    def _process_recognition(self, node, extras):
        pass


# def create_grammar():
#     grammar = Grammar("files")
#     return grammar, True
