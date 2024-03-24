from enum import Enum

from modules.booléen import BooleanExpr
from modules.entier import ArithmeticExpression
from modules.texte import StringExpression
from modules.wrapper import Wrapper


def integer_atomic_value(args):
    return int(args)


class Expression(Enum):
    """
    Expression:
        used to define how operations are defined on values
    """

    INTEGER = Wrapper(integer_atomic_value)
    STRING = Wrapper(StringExpression)
    BOOLEAN = Wrapper(BooleanExpr)
