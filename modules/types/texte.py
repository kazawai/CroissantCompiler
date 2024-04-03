from enum import Enum

from modules.utils.wrapper import Wrapper
from modules.exceptions.exception import SPFIndexError


def string_atomic_value(args):
    return args[1:len(args) - 1]

def concat(args):
    return args[0] + args[1]

def size(args):
    return len(args[0])

def index(args):
    if args[1] < 0 or args[1] >= len(args[0]):
        raise SPFIndexError(args[1], len(args[0]))
    return args[0][args[1]]

class StringExpression(Enum):
    """
    String Expr:
        used to define how operations are defined on string values
    """
    STRING_ATOMIC_VALUE = Wrapper(string_atomic_value)
