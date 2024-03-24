from enum import Enum
from wrapper import Wrapper
from sys import getsizeof
import booléen, entier, texte

TYPES = {"booléen" : booléen, "entier" : entier, "texte" : texte}

class Variable():

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
        print(args)
        return Variable(args[1], args[0], args[2])

    @staticmethod
    def declaration(args):
        return Variable(args[1], args[0], None)


class VariableExpression(Enum):
    DECLARATION = Wrapper(Variable.declaration)
    INSTANCIATION = Wrapper(Variable.instanciation)
