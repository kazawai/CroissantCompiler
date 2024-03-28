from enum import Enum

from modules.wrapper import Wrapper


def int_atomic_value(args):
    if isinstance(args, list):
        args = args[0]
    return int(args)


def int_negation(args):
    print(args)
    return -args[0]


def arithmetic_op(args, operation):
    return operation(args[0], args[1])


class ArithmeticExpression(Enum):
    """
    Arithmetic Expr:
        used to define how operations are defined on integer values
    """

    INT_ATOMIC_VALUE = Wrapper(int_atomic_value)
    INT_NEGATION = Wrapper(int_negation)
    ADDITION = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x + y))
    SUBTRACTION = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x - y))
    MULTIPLICATION = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x * y))
    DIVISION = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x // y))
    EQUALS = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x == y))
    NOT_EQUAL = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x != y))
