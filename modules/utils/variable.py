import sys
from enum import Enum

from modules.exceptions.exception import (SPFAlreadyDefined,
                                          SPFIncompatibleType,
                                          SPFUninitializedVariable,
                                          SPFUnknowVariable,
                                          SPFBadIdentifier)
from modules.utils import global_var
from modules.utils.wrapper import Wrapper

TYPES = {"booléen": bool, "entier": int, "texte": str, "liste": list, "{": dict}
KEYWORDS = list(TYPES.keys())[:len(list(TYPES.keys())) - 1] + ["faux", "vrai", "while", "for", "soit", "ajouter", "dans", "sortir"]


class Variable:
    """
    Representation of variable inside spf programm
    """

    def __init__(self, label, type_, value=None, debug=True):
        """
        Instanciate an object variable base on the given parameters:
        
        PARAM
        -----
            - label : the name of the variable
            - type_ : the type of it 
            - value : the value (might be none if declaration rule)
            - debug : flag to get info of the variable instanciation 

        CONDITIONS
        ----------
            - The variable cannot have as label a keyword.
            - The variable cannot be redefined.
            - The type of the value and the type of the variable must match for instanciation rule
        """
        context = get_context()
        if label in KEYWORDS:
            raise SPFBadIdentifier(label)
        if label in context.keys():
            raise SPFAlreadyDefined(label)
        if value != None and TYPES[type_] != type(value):
            raise SPFIncompatibleType(label, type_, value)
        if debug and global_var.debug:
            if value == None:
                print(
                    f"DEBUG LIGNE {global_var.line_counter} : déclare {type_} {label} = vide",
                    file=sys.stderr,
                )
            else:
                print(
                    f"DEBUG LIGNE {global_var.line_counter} : déclare {type_} {label} = {value}",
                    file=sys.stderr,
                )

        self.label = label
        self.type = type_
        self.value = value
        context[self.label] = self

    def __str__(self):
        """
        Basic overriding method of the print object function
        """
        if self.value == True:
            return f"{self.type} {self.label} = vrai"
        if self.value == False:
            return f"{self.type} {self.label} = faux"
        return f"{self.type} {self.label} = {self.value}"

    def pop(self):
        """
        Remove the variable from the context (like free() in C)
        """
        del get_context()[self.label]

    @staticmethod
    def instanciation(args):
        """
        Instanciation rule : create a variable with given value
        """
        var = Variable(args[1], args[0], args[2])
        return var

    @staticmethod
    def declaration(args):
        """
        Declaration rule : declare a variable with no value specified
        """
        var = Variable(args[1], args[0], None)
        return var

    @staticmethod
    def call(args):
        """
        Call rule : return the value of an existing variable from the context
        """
        context = global_var.context
        i = 0
        while i < global_var.nested_counter and args not in context.keys():
            context = context["{"].value
            i += 1
        try:
            if context[args].value != None:
                var = context[args]
                if global_var.debug:
                    print(
                        f"DEBUG LIGNE {global_var.line_counter} : accède {var.type} {var.label} = {var.value}",
                        file=sys.stderr,
                    )
                return var.value
            raise SPFUninitializedVariable(args)
        except KeyError:
            raise SPFUnknowVariable(args)

    @staticmethod
    def modification(args):
        """
        Modification rule : modify the value stored inside an existing variable from the context
        """
        context = global_var.context
        i = 0
        while i < global_var.nested_counter and not args[0] in context.keys():
            context = context["{"].value
            i += 1
        try:
            var = context[args[0]]
            if TYPES[var.type] != type(args[1]):
                raise SPFIncompatibleType(var.label, var.type, args[1])
            var.value = args[1]
            if global_var.debug:
                print(
                    f"DEBUG LIGNE {global_var.line_counter} : modifie {var.type} {var.label} = {var.value}",
                    file=sys.stderr,
                )
        except KeyError:
            raise SPFUnknowVariable(args)

    @staticmethod
    def is_variable(label):
        """
        Used to check if a variable is present inside the context
        """
        current_context = global_var.context
        i = 0
        while i < global_var.nested_counter:
            if label in current_context.keys():
                return True
            current_context = current_context["{"].value
            i += 1
        return False


class Block(Variable):
    """
    A block represent a code part in wich the context must be restrained (such as if, while,etc)
    """

    def __init__(self):
        """
        Instanciate Block as variable. This have fixed label and value.
        """
        if global_var.debug:
            print(
                f"DEBUG LIGNE {global_var.line_counter} : entrée d'un bloc",
                file=sys.stderr,
            )
        super().__init__("{", "{", {}, False)
        global_var.nested_counter += 1

    def pop(self):
        """
        Remove the block from the context resulting in the loss of values contained
        inside this block.
        """
        if global_var.debug:
            print(
                f"DEBUG LIGNE {global_var.line_counter} : sortie d'un bloc",
                file=sys.stderr,
            )
        context = global_var.context
        i = 0
        while i < global_var.nested_counter - 1:
            context = context[self.label].value
            i += 1
        del context[self.label]
        global_var.nested_counter -= 1

    @staticmethod
    def new_block(_):
        """
        return instance of new block
        """
        return Block()


def get_context():
    """
    Give the current context in wich we are inside the program.
    This goes through the different blocks to find the most nested one.
    """
    current_context = global_var.context
    i = 0
    while i < global_var.nested_counter:
        current_context = current_context["{"].value
        i += 1
    if type(current_context) == dict:
        return current_context
    return current_context.value


class VariableExpression(Enum):
    """
    Enum of possible variable expressions
    """
    DECLARATION = Wrapper(Variable.declaration)
    INITIALIZATION = Wrapper(Variable.instanciation)
    CALL = Wrapper(Variable.call)
    MODIFICATION = Wrapper(Variable.modification)
    BLOCK = Wrapper(lambda args: None)
