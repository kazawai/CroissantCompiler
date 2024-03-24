from enum import Enum

from modules.wrapper import Wrapper


def int_atomic_value(args):
    return int(args)


def negation(args):
    return -int_atomic_value(args)


def arithmetic_op(args, operation):
    return operation(args[0], args[1])


class ArithmeticExpression(Enum):
    """
    Arithmetic Expr:
        used to define how operations are defined on integer values
    """

    INTEGER_ATOMIC_VALUE = Wrapper(int_atomic_value)
    NEGATION = Wrapper(negation)
    ADDITION = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x + y))
    SUBTRACTION = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x - y))
    MULTIPLICATION = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x * y))
    DIVISION = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x / y))
    EQUAL = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x == y))
    NOT_EQUAL = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x != y))
    GREATER = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x > y))
    LESS = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x < y))
    GREATER_EQUAL = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x >= y))
    LESS_EQUAL = Wrapper(lambda args: arithmetic_op(args, lambda x, y: x <= y))
