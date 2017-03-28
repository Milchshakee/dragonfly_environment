import os
from modules.util.json_parser import parse_file
from dragonfly import (Grammar, Choice, RuleRef, DictListRef,
                       Dictation, Compound, Rule, CompoundRule,
                       DictList, Alternative)

data = []
rules = []
required_parameters = []
parameters_values = {}
active_executable = None
active_configuration = None
active_parameter_rules = []


class CommandRule(CompoundRule):

    def __init__(self, command_name, executable, configuration, parameter_rules):
        self.__executable = executable
        self.__configuration = configuration
        self.__parameter_rules = parameter_rules
        configuration_name = configuration["name"] if not configuration["name"] == "default" else ""
        CompoundRule.__init__(self, spec=command_name + " " + configuration_name)

    def _process_recognition(self, node, extras):
        default_parameters = {}
        for parameter in self.__configuration["params"]:
            default_parameters[parameter["name"]] = parameter["default"]
            if parameter["required"] is True:
                required_parameters.append(parameter["name"])
        global parameters_values
        parameters_values = default_parameters
        for rule in self.__parameter_rules:
            rule.enable()
        global active_parameter_rules
        active_parameter_rules = self.__parameter_rules
        global active_executable
        active_executable = self.__executable
        global active_configuration
        active_configuration = self.__configuration


class ParameterRule(CompoundRule):

    def __init__(self, command_name, configuration_name, parameter):
        self.__parameter = parameter
        spec = None
        extras = []
        if parameter["type"] == "dictation":
            spec = "set " + parameter["name"] + " <value>"
            extras = [Dictation("value")]
        if parameter["type"] == "alternative":
            values = parameter["values"]
            if isinstance(values, dict):
                extras = [Choice("value", values)]
            if isinstance(values, list):
                extras = [Alternative(name="value", children=[Compound(spec=word, value=word) for word in values])]
            spec = "set " + parameter["name"] + " <value>"
        if parameter["type"] == "switch-enable":
            spec = "enable " + parameter["name"]
        if parameter["type"] == "switch-disable":
            spec = "disable " + parameter["name"]

        CompoundRule.__init__(self,
                              name=command_name + "." + configuration_name + "." + parameter["name"],
                              spec=spec,
                              extras=extras)

    def _process_recognition(self, node, extras):
        if self.__parameter["name"] in required_parameters:
            required_parameters.remove(self.__parameter["name"])

        if "value" in extras:
            value = extras["value"]
            format_string = self.__parameter["format"]
            string = format_string.replace("<value>", str(value))
            parameters_values[self.__parameter["name"]] = string
        else:
            parameters_values[self.__parameter["name"]] = self.__parameter["value"]


class ExecuteRule(CompoundRule):

    spec = "execute command"

    def _process_recognition(self, node, extras):
        global active_executable
        global active_configuration
        if active_executable is None:
            print("No command to execute")
            return
        if len(required_parameters) > 0:
            print("Missing required parameters: " + required_parameters)
            return

        command = active_executable + " " + active_configuration["args"]
        for value in parameters_values.itervalues():
            if value is not None:
                command += " " + value
        print(command)

        global active_parameter_rules
        for rule in active_parameter_rules:
            rule.disable()
        active_parameter_rules = []
        active_executable = None
        active_configuration = None

default_programs_file = """{
    "special_words": ["word1", "some text", "etc"]
}
"""


def reload_config(config_path):
    programs_file = os.path.join(config_path, "programs.json")
    global data
    data = parse_file(programs_file, default_programs_file)["commands"]
    for command in data:
        if not command.has_key("configurations"):
            default_configuration = {"name": "default", "args": None, "params": []}
            command["configurations"] = [default_configuration]
        else:
            for configuration in command["configurations"]:
                if "args" not in configuration:
                    configuration["args"] = None
                if "params" not in configuration:
                    configuration["params"] = []
                else:
                    for parameter in configuration["params"]:
                        if "required" not in parameter:
                            parameter["required"] = False
                        if "default" not in parameter:
                            parameter["default"] = None


def create_grammar():
    grammar = Grammar("program")

    for command in data:
        for configuration in command["configurations"]:
            default_parameters = {}
            parameters_rules = []
            for parameter in configuration["params"]:
                default_parameters[parameter["name"]] = parameter["default"]
                rule = ParameterRule(command["name"], configuration["name"], parameter)
                grammar.add_rule(rule)
                rule.disable()
                parameters_rules.append(rule)

            rules.extend(parameters_rules)
            grammar.add_rule(CommandRule(command["name"], command["path"], configuration, parameters_rules))
    grammar.add_rule(ExecuteRule())
    return grammar, True
