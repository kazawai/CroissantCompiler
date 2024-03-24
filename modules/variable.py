from enum import Enum
from sys import getsizeof

import modules.booléen as booléen
import modules.entier as entier
import modules.texte as texte
from modules.wrapper import Wrapper

TYPES = {"booléen": booléen, "entier": entier, "texte": texte}


class Variable:

    def __init__(self, label, type, value):
        if not type in TYPES.keys():
            raise Exception(f"unknown type {type}")
        self.label = label
        self.type = type
        self.value = value

    def __str__(self):
        return f"""objet variable : \n
      label -> {self.label} \n
      type -> {self.type}\n
      valeur -> {self.value}\n
      taille en mémoire -> {getsizeof(self)} octets"""

    @staticmethod
    def instanciation(args):
        var = Variable(args[1], args[0], args[2])
        args[3].update({args[1]: var})
        return var

    @staticmethod
    def declaration(args):
        var = Variable(args[1], args[0], None)
        args[2].update({args[1]: var})
        return var


class VariableExpression(Enum):
    DECLARATION = Wrapper(Variable.declaration)
    INITIALIZATION = Wrapper(Variable.instanciation)
    VARIABLE = Wrapper(lambda args: args[1].find(args[0]).value)
