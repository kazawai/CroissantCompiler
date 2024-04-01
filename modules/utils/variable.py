from enum import Enum
from modules.utils import global_var
from modules.exceptions.exception import SPFUnknowVariable, SPFUninitializedVariable, SPFAlreadyDefined, SPFIncompatibleType
from modules.utils.wrapper import Wrapper

TYPES = {"booléen": bool, "entier": int, "texte": str, "liste": list}
KEYWORDS = list(TYPES.keys()) + ["faux", "vrai", "while", "for"]

class Variable:

    def __init__(self, label, type_, value=None):
        if global_var.debug:
            if value == None:
                print(f"{global_var.line_counter} : déclare {type_} {label} = vide")
            else:
                print(f"{global_var.line_counter} : déclare {type_} {label} = {value}")
        if label in global_var.context.keys():
            raise SPFAlreadyDefined(label)
        if value != None and TYPES[type_] != type(value):
            raise SPFIncompatibleType(label, type_, value)
        self.label = label
        self.type = type_
        self.value = value
        global_var.context[label] = self

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
    
    @staticmethod
    def call(args):
        try:
            if global_var.context[args].value != None:
                return global_var.context[args].value
            raise SPFUninitializedVariable(args)
        except KeyError:
            raise SPFUnknowVariable(args)
    
    @staticmethod
    def modification(args):
        try:
            global_var.context[args[0]].value = args[1]
        except KeyError:
            raise SPFUnknowVariable(args)


class VariableExpression(Enum):
    DECLARATION = Wrapper(Variable.declaration)
    INITIALIZATION = Wrapper(Variable.instanciation)
    CALL = Wrapper(Variable.call)
    MODIFICATION = Wrapper(Variable.modification)
