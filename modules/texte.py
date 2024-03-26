from enum import Enum

from modules.wrapper import Wrapper


def string_atomic_value(args):
    return args[1:len(args) - 1]

def concat(args):
    return args[0] + args[1]

def size(args):
    return len(args)

def index(args):
    return args[0][args[1]]

class StringExpression(Enum):
    """
    String Expr:
        used to define how operations are defined on string values
    """

    STRING_ATOMIC_VALUE = Wrapper(string_atomic_value)
    CONCAT = Wrapper(concat)
    SIZE = Wrapper(size)
    INDEX = Wrapper(index)
