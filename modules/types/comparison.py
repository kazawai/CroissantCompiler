from enum import Enum

from modules.utils.wrapper import Wrapper

class ComparisonExpression(Enum):
    """
    Arithmetic Expr:
        used to define how operations are defined on integer values
    """

    EQUALS = Wrapper(lambda args: args[0] == args[1])
    NOT_EQUAL = Wrapper(lambda args: args[0] != args[1])
    GREATER = Wrapper(lambda args: args[0] > args[1], authorized_types={int : [int]}, label_op=">")
    LESS = Wrapper(lambda args: args[0] < args[1], authorized_types={int : [int]}, label_op="<")
    GREATER_EQUAL = Wrapper(lambda args: args[0] >= args[1], authorized_types={int : [int]}, label_op=">=")
    LESS_EQUAL = Wrapper(lambda args: args[0] <= args[1], authorized_types={int : [int]}, label_op="<=")
