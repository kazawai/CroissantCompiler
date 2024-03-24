from enum import Enum
from wrapper import Wrapper

def boolean_atomic_value(args):
    match args:
        case "faux":
            return False
        case "vrai":
            return True
        case _:
            raise Exception(f"the atomic value <{args}> of boolean is not defined ")

def negation(args):
    return not args

def conjunction(args):
    return args[0] and args[1]

def disjunction(args):
    return args[0] or args[1]


class BooleanExpr(Enum):
    """
    Boolean Expr:
        used to define how operations are defined on boolean values
    """
    BOOLEAN_ATOMIC_VALUE = Wrapper(boolean_atomic_value)
    NEGATION = Wrapper(negation)
    CONJUNCTION = Wrapper(conjunction)
    DISJUNCTION = Wrapper(disjunction)
