from enum import Enum
from sys import getsizeof

from modules.wrapper import Wrapper

TYPES = {"booléen": bool, "entier": int, "texte": str, "liste": list}
KEYWORDS = list(TYPES.keys()) + ["faux", "vrai", "while", "for"]

global global_context
global_context = {}


class Variable:

    def __init__(self, label, type, value):
        if not type in TYPES.keys():
            raise Exception(f"unknown type {type}")
        if label in KEYWORDS:
            raise Exception(f"cannot assign keyword as label")
        self.label = label
        self.type = type
        self.value = value
        global_context[label] = self

    def __str__(self):
        if self.value == True:
            return f"{self.type} {self.label} = vrai"
        if self.value == False:
            return f"{self.type} {self.label} = faux"
        return f"{self.type} {self.label} = {self.value}"

    def __add__(self, other):
        if isinstance(other, Variable):
            return VariableExpression.VARIABLE.value(other.label).value + self.value
        return self.value + other

    @staticmethod
    def instanciation(args):
        var = Variable(args[1], args[0], args[2])
        return var

    @staticmethod
    def declaration(args):
        var = Variable(args[1], args[0], None)
        return var


class VariableExpression(Enum):
    DECLARATION = Wrapper(Variable.declaration)
    INITIALIZATION = Wrapper(Variable.instanciation)
    VARIABLE = Wrapper(lambda args: global_context[args])
