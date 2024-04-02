from enum import Enum
from modules.utils import global_var
from modules.exceptions.exception import SPFUnknowVariable, SPFUninitializedVariable, SPFAlreadyDefined, SPFIncompatibleType
from modules.utils.wrapper import Wrapper
import sys

TYPES = {"booléen": bool, "entier": int, "texte": str, "liste": list, "{" : dict}
KEYWORDS = list(TYPES.keys()) + ["faux", "vrai", "while", "for"]

class Variable:

    def __init__(self, label, type_, value=None):
        if global_var.debug:
            if value == None:
                print(f"DEBUG: ligne {global_var.line_counter} : déclare {type_} {label} = vide", file=sys.stderr)
            else:
                print(f"DEBUG: ligne {global_var.line_counter} : déclare {type_} {label} = {value}", file=sys.stderr)
        if label in global_var.context.keys():
            raise SPFAlreadyDefined(label)
        if value != None and TYPES[type_] != type(value):
            raise SPFIncompatibleType(label, type_, value)
        self.label = label
        self.type = type_
        self.value = value
        get_context()[self.label] = self

    def __str__(self):
        if self.value == True:
            return f"{self.type} {self.label} = vrai"
        if self.value == False:
            return f"{self.type} {self.label} = faux"
        return f"{self.type} {self.label} = {self.value}"

    def pop(self):
        del get_context()[self.label]

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
        context = global_var.context
        i = 0
        while i < global_var.nested_counter and args not in context.keys():
            context = context['{'].value
            i += 1
        try:
            if context[args].value != None:
                var = context[args]
                if global_var.debug:
                    print(f"DEBUG: ligne {global_var.line_counter} : accède {var.type} {var.label} = {var.value}", file=sys.stderr)
                return var.value
            raise SPFUninitializedVariable(args)
        except KeyError:
            raise SPFUnknowVariable(args)
    
    @staticmethod
    def modification(args):
        context = global_var.context
        i = 0
        while i < global_var.nested_counter and args not in context.keys():
            context = context['{'].value
            i += 1
        context = get_context()
        try:
            context[args[0]].value = args[1]
            var = context[args[0]]
            if global_var.debug:
                print(f"DEBUG: ligne {global_var.line_counter} : modifie {var.type} {var.label} = {var.value}", file=sys.stderr)
        except KeyError:
            raise SPFUnknowVariable(args)     
    

    
class Block(Variable):

    def __init__(self):
        super().__init__('{','{', {})
        global_var.nested_counter += 1

    def pop(self):
        context = global_var.context
        i = 0
        while i < global_var.nested_counter - 1:
            context = context[self.label].value
            i += 1
        del context[self.label]
        global_var.nested_counter -= 1

    @staticmethod
    def new_block(_):
        return Block()

def get_context():
    current_context = global_var.context
    i = 0
    while i < global_var.nested_counter:
        current_context = current_context['{'].value
        i += 1
    if type(current_context) == dict:
        return current_context
    return current_context.value

class VariableExpression(Enum):
    DECLARATION = Wrapper(Variable.declaration)
    INITIALIZATION = Wrapper(Variable.instanciation)
    CALL = Wrapper(Variable.call)
    MODIFICATION = Wrapper(Variable.modification)
    BLOCK = Wrapper(lambda args : None)