from enum import Enum

from modules.utils.wrapper import Wrapper


class StringExpression(Enum):
    """
    String Expr:
        used to define how operations are defined on string values
    """

    STRING_ATOMIC_VALUE = Wrapper(lambda args: args[1 : len(args) - 1])
    SIZE_TEXT = Wrapper(lambda args: len(args[1]))
