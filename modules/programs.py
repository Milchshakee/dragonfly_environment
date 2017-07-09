import os
import subprocess

from win32process import DETACHED_PROCESS
from dragonfly import Choice, Grammar, CompoundRule
from modules.util.json_parser import parse_file


programs = {}


class ProgramRule(CompoundRule):

    spec = "open <program>"

    def __init__(self):
        CompoundRule.__init__(self, extras=[Choice("program", programs)])

    def _process_recognition(self, node, extras):
        path = extras["program"]
        subprocess.Popen([path], creationflags=DETACHED_PROCESS)


default_configuration = {
    "programs": [
        {
            "name": "python editor",
            "path": "full\\path"
        }
    ]
}


def load_config(config_path):
    global programs
    programs_list = parse_file(os.path.join(config_path, "programs.json"), default_configuration)["programs"]
    for program in programs_list:
        programs[program["name"]] = program["path"]


def create_grammar():
    grammar = Grammar("programs")
    grammar.add_rule(ProgramRule())
    grammar.load()
    return grammar, True

