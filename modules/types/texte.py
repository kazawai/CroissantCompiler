from enum import Enum

from modules.exceptions.exception import SPFIndexError
from modules.utils.wrapper import Wrapper


def index_string(args):
    index = args[1] 
    if index < 1 or index > len(args[0]) - 2:
        raise SPFIndexError(index, len(args[0]) - 3)
    return args[0].strip('"')[index - 1]


class StringExpression(Enum):
    """
    String Expr:
        used to define how operations are defined on string values
    """

    STRING_ATOMIC_VALUE = Wrapper(lambda args: args[1 : len(args) - 1])
    SIZE_STRING = Wrapper(lambda args: len(args[1]))
    INDEX_STRING = Wrapper(index_string)
    CONCAT_STRING = Wrapper(lambda args: args[0] + args[1])
