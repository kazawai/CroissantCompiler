from enum import Enum

from modules.utils.wrapper import Wrapper


def int_atomic_value(args):
    if isinstance(args, list):
        args = args[0]
    return int(args)


def int_negation(args):
    return -args[0]


class ArithmeticExpression(Enum):
    """
    Arithmetic Expr:
        used to define how operations are defined on integer values
    """

    INT_ATOMIC_VALUE = Wrapper(int_atomic_value)
    
    INT_NEGATION = Wrapper(lambda arg : arg[0], {int : []}, label_op="-")
    ADDITION = Wrapper(lambda args:  args[0] + args[1], {int: [int], list:[list], str:[str]}, label_op="+")
    SUBTRACTION = Wrapper(lambda args: args[0] - args[1], {int : [int]}, label_op="-")
    MULTIPLICATION = Wrapper(lambda args: args[0] * args[1], {int : [int]}, label_op="*")
    DIVISION = Wrapper(lambda args: args[0] // args[1], {int : [int]}, label_op="/")
