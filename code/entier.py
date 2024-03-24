from enum import Enum
from wrapper import Wrapper

def integer_atomic_value(args):
    return int(args)

def negation(args):
    return - integer_atomic_value(args)

def plus(args):
    return args[0] + args[1]

def minus(args):
    return plus([args[0], negation(args[1])])

def div(args):
    return args[0] // args[0]

def mul(args):
    return args[0] * args[0]

def gt(args):
    return args[0] < args[1]

def lt(args):
    return args[0] > args[1]

def gte(args):
    return args[0] <= args[1]

def lte(args):
    return args[0] >= args[1]

class ArithmeticExpression(Enum):
    """
    Arithmetic Expr:
        used to define how operations are defined on integer values
    """
    INTEGER_ATOMIC_VALUE = Wrapper(integer_atomic_value)
    NEGATION = Wrapper(negation)
    PLUS = Wrapper(plus)
    MINUS = Wrapper(minus)
    DIV = Wrapper(div)
    MUL = Wrapper(mul)
    GT = Wrapper(gt)
    LT = Wrapper(lt)
    GTE = Wrapper(gte)
    LTE = Wrapper(lte)
