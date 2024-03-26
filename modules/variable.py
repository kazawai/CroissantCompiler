from enum import Enum
from sys import getsizeof

import modules.booléen as booléen
import modules.entier as entier
import modules.texte as texte
from modules.wrapper import Wrapper

TYPES = {"booléen": booléen, "entier": entier, "texte": texte}
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
        return f"""objet variable : \n
      label -> {self.label} \n
      type -> {self.type}\n
      valeur -> {self.value}\n
      taille en mémoire -> {getsizeof(self)} octets\n
      global_context -> {global_context}"""

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
