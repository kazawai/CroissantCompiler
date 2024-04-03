from enum import Enum

from modules.utils.wrapper import Wrapper

VALUES = {"faux" : False, "vrai" : True, False : "faux", True : "vrai"}

def bool_atomic_value(args):
    match args:
        case "faux":
            return False
        case "vrai":
            return True
        case _:
            raise Exception(f"the atomic value <{args}> of boolean is not defined ")


def bool_negation(args):
    return not args[0]


def conjunction(args):
    return args[0] and args[1]


def disjunction(args):
    return args[0] or args[1]


class BooleanExpression(Enum):
    """
    Boolean Expr:
        used to define how operations are defined on boolean values
    """

    BOOL_ATOMIC_VALUE = Wrapper(bool_atomic_value)
    BOOL_NEGATION = Wrapper(bool_negation, authorized_types={bool:[bool]}, label_op="non")
    CONJUNCTION = Wrapper(conjunction, authorized_types={bool:[bool]}, label_op="et")
    DISJUNCTION = Wrapper(disjunction, authorized_types={bool:[bool]}, label_op="ou")