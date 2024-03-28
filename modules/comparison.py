from enum import Enum

from modules.variable import global_context
from modules.wrapper import Wrapper


def get_var_value(var):
    if var in global_context:
        return global_context[var].value
    return var


def comparison_op(args, operation):
    args = [get_var_value(arg) for arg in args]
    return operation(args)


class ComparisonExpression(Enum):
    """
    Arithmetic Expr:
        used to define how operations are defined on integer values
    """

    EQUALS = Wrapper(lambda args: args[0] == args[1])
    NOT_EQUAL = Wrapper(lambda args: args[0] != args[1])
    GREATER = Wrapper(lambda args: comparison_op(args, lambda args: args[0] > args[1]))
    LESS = Wrapper(lambda args: comparison_op(args, lambda args: args[0] < args[1]))
    GREATER_EQUAL = Wrapper(
        lambda args: comparison_op(args, lambda args: args[0] >= args[1])
    )
    LESS_EQUAL = Wrapper(
        lambda args: comparison_op(args, lambda args: args[0] <= args[1])
    )
